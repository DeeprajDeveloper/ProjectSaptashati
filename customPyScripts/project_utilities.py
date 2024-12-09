from pdf2image import convert_from_path
from PIL import Image
import pytesseract as pt
import re
import os
import sqlite3 as sql
import customPyScripts.constants as const
import logging
import inspect
from flask import jsonify
import traceback

# Configure logging
logging.basicConfig(format='[%(levelname)s] [%(asctime)s] - %(message)s', level=logging.INFO)


def log_message(level, message, call_type):
    """
    Logs a message with the function name dynamically.
    OPTIONS: info/error/debug/warning
    """
    function_name = inspect.currentframe().f_back.f_code.co_name
    full_message = f"[{call_type}] {function_name}(): {message}"
    if level == "info":
        logging.info(full_message)
    elif level == "error":
        logging.error(full_message)
    elif level == "debug":
        logging.debug(full_message)
    elif level == "warning":
        logging.warning(full_message)


def convert_pdf_pages_to_images(input_path, output_path, image_name):
    print(f"[project_utility.py] Loading PDF file to generate images")
    images = convert_from_path(input_path)
    if image_name is None:
        image_name = "output_image_page"
    for index, image in enumerate(images):
        image_path = f"{output_path}/{image_name}_{index+1}.jpg"
        image.save(image_path, 'JPEG')
        print(f"[project_utility.py] Converting Page {index}. Saving image to {output_path}")


def rename_files(find_text, replace_text_with, folder_path):
    files_list = os.listdir(folder_path)
    for file in files_list:
        new_filename = file.replace(find_text, replace_text_with)
        print(f"[project_utility.py] Renaming file {file}")
        os.rename(fr'{folder_path}\{file}', fr'{folder_path}\{new_filename}')


def reformat_digits_in_filename(zero_fill, folder_path):
    print('[project_utility.py] Reformatting digits in filename')
    files_list = os.listdir(folder_path)
    new_filenames_list = []
    for file in files_list:
        digit = re.findall(r'\d+', file)
        formatted_digit = digit[0].zfill(zero_fill)
        new_filename = file.replace(digit[0], formatted_digit)
        new_filenames_list.append(new_filename)
        os.rename(fr'{folder_path}\{file}', fr'{folder_path}\{new_filename}')
    print('[project_utility.py] Reformatting digits in filename is completed.')


def ocr_image_reader_to_text(images_folder, output_text):
    print('[project_utility.py] Reading images using OCR to append data in text file')
    file_list = os.listdir(images_folder)
    file_list.sort()
    data_list = []
    page_counter = 1
    for img_file_name in file_list:
        print(f'{page_counter} - {img_file_name} - Reading Image')
        image_file = fr'{images_folder}\{img_file_name}'

        image = Image.open(image_file)
        text = pt.image_to_string(image, lang='hin')
        data_list.append(text)
        print(f'{page_counter} - {img_file_name} - OCR Complete')

        with open(output_text, 'w', encoding='utf-8') as file:
            file.writelines(data_list)
            file.writelines(f"--------------------[{page_counter}]--------------------\n")

        print(f'{page_counter} - {img_file_name} - Data loaded in a .txt file')
        page_counter += 1


def sqlite_execute_script(database, sql_script):
    sqlite_connection = sql.connect(database=database)
    try:
        sqlite_connection.executescript(sql_script)
        status = True
        return status
    except Exception as error:
        status = False
        print(f"Error Message: {str(error)}")
        return status


def sqlite_check_if_exists(database, sql_script):
    sqlite_connection = sql.connect(database=database)
    try:
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute(sql_script)
        sql_data = sqlite_cursor.fetchone()
        # print(sql_data)
        if sql_data is not None:
            status = True if sql_data[0] >= 1 else False
        else:
            status = False
        # print(status)
        return status
    except Exception as error:
        print(f"Error Message: {str(error)}")
        return False


def sqlite_retrieve_data(database, sql_script):
    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]
    try:
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute(sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")


def sqlite_retrieve_data_custominput(database, sql_script, data_input):
    sqlite_connection = sql.connect(database=database)
    # sqlite_connection.row_factory = lambda cursor, row: row[0]
    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?', str(data_input))
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")


def sqlite_get_data_custominput_rowsonly(database, sql_script, data_input):
    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]
    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?', data_input)
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")


def return_verse_json(result_set, verse_type, verse_id, name):
    data_list = []
    latin_translation = []
    additional_context = {}
    meanings = ['', '']
    error_message = None
    error_type = None
    json_response = None

    log_message("info", "(1) Generation of JSON response Initiated.", call_type='UTIL')
    if result_set is not None:
        for item in result_set:
            if verse_type == 'introduction':
                latin_translation = sqlite_get_data_custominput_rowsonly(database=const.DATABASE_FILE, sql_script=const.SQL__GET_TRANSLATION_INTRO_EXIT, data_input=str(item[2]))
                meanings = sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_MEANING_INTRO_EXIT, data_input=str(item[2]))[0]
                if verse_id == '':
                    storta_name = name
                else:
                    intro_details = sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_STOTRA_NAME, data_input=str(verse_id))[0]
                    storta_name = intro_details[0] if (intro_details[1] is None or intro_details[1] == "") else f"{intro_details[0]} - {intro_details[1]}"
                additional_context = {'stortaName': storta_name}
            elif verse_type == 'chapters' or verse_type == 'chapter':
                latin_translation = sqlite_get_data_custominput_rowsonly(database=const.DATABASE_FILE, sql_script=const.SQL__GET_TRANSLATION_CHAPTERS, data_input=str(item[2]))
                if verse_id == '':
                    additional_context = {'chapterName': name}
                else:
                    chapter_details = sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTER_NAME, data_input=str(verse_id))[0]
                    additional_context = {'chapterName': chapter_details[0], 'charitraName': chapter_details[1]}
            elif verse_type == 'conclusion':
                latin_translation = sqlite_get_data_custominput_rowsonly(database=const.DATABASE_FILE, sql_script=const.SQL__GET_TRANSLATION_INTRO_EXIT, data_input=str(item[2]))

            item_json = {
                'id': item[2],
                'verseNo': item[1] if item[1] is not None else '',
                'verseDetails': {
                    'devanagariShloka': item[0],
                    'translationIAST': latin_translation[0],
                },
                'meanings': {
                    'englishMeaning': meanings[0],
                    'hindiMeaning': meanings[1]
                },
                'additionalContext': additional_context
            }

            data_list.append(item_json)

        if len(data_list) == 0:
            log_message("warning", "(x) Something went wrong. No data retrieved for the inputs provided", call_type='UTIL')
            data_values = []
            if verse_type == 'introduction':
                data_values = sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_INTRO_MIN_MAX, data_input='')
            elif verse_type == 'chapters' or verse_type == 'chapter':
                data_values = sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTERS_MIN_MAX, data_input='')
            elif verse_type == 'conclusion':
                data_values = sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_EXIT_MIN_MAX, data_input='')
            error_type = 'VerseIDOutOfBounds'
            error_message = f'No data available. Verse ID must be between {data_values[0]} for {verse_type}'

        log_message("info", "(2) Populating standard JSON response template", call_type='UTIL')
        json_response = response_template(is_Error=False, success=True, data=data_list, message='Data Retrieved Successfully.', error_type=error_type, error_stack_trace=error_message)
        log_message("info", "(3) Returning JSON response for further processing", call_type='UTIL')
    return json_response


def response_template(success=True, message="", data=None, error_type=None, error_stack_trace=None, status_code=200, is_Error=False):
    """
    Creates a standardized JSON response.

    :param success: Whether the request was successful.
    :param message: A message string.
    :param data: The response payload (default: None).
    :param error_type: Error Type (default: None).
    :param error_stack_trace:Error Stacktrace
    :param status_code: HTTP status code (default: 200).
    :param is_Error: A Boolean flag that indicates if the error is from a Exception class or not.
    :return: Flask Response object.
    """

    response_body = {
        "responseInformation": {
            "statusCode": status_code,
            "statusDescription": "success" if success else "failure",
            "messageText": message,
            "errorStacktrace": {
                "errorCode": f"{type(error_type).__name__}: {str(error_type)}" if is_Error else error_type,
                "errorMessage": error_stack_trace
            }
        },
        "dataExtract": data
    }
    response_body = {k: v for k, v in response_body.items() if v is not None}  # Remove None values
    return jsonify(response_body), status_code
