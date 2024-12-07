from pdf2image import convert_from_path
from PIL import Image
import pytesseract as pt
import re
import os
import sqlite3 as sql


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
        os.rename(f'{folder_path}\{file}', f'{folder_path}\{new_filename}')


def reformat_digits_in_filename(zero_fill, folder_path):
    print('[project_utility.py] Reformatting digits in filename')
    files_list = os.listdir(folder_path)
    new_filenames_list = []
    for file in files_list:
        digit = re.findall(r'\d+', file)
        formatted_digit = digit[0].zfill(zero_fill)
        new_filename = file.replace(digit[0], formatted_digit)
        new_filenames_list.append(new_filename)
        os.rename(f'{folder_path}\{file}', f'{folder_path}\{new_filename}')
    print('[project_utility.py] Reformatting digits in filename is completed.')


def ocr_image_reader_to_text(images_folder, output_text):
    print('[project_utility.py] Reading images using OCR to append data in text file')
    file_list = os.listdir(images_folder)
    file_list.sort()
    data_list = []
    page_counter = 1
    for img_file_name in file_list:
        print(f'{page_counter} - {img_file_name} - Reading Image')
        image_file = f'{images_folder}\{img_file_name}'

        image = Image.open(image_file)
        text = pt.image_to_string(image, lang='hin')
        data_list.append(text)
        print(f'{page_counter} - {img_file_name} - OCR Complete')

        with open(output_text, 'w', encoding='utf-8') as file:
            file.writelines(data_list)
            file.writelines(f"--------------------[{page_counter}]--------------------\n")

        print(f'{page_counter} - {img_file_name} - Data loaded in a .txt file')
        page_counter += 1


# ------------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------------
def sqlite_retrieve_data(database, sql_script):
    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]
    try:
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute(sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as error:
        print(f"Error Message: {str(error)}")


# ------------------------------------------------------------------------------------
def sqlite_retrieve_data_custominput(database, sql_script, data_input):
    sqlite_connection = sql.connect(database=database)
    # sqlite_connection.row_factory = lambda cursor, row: row[0]
    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?', str(data_input))
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as error:
        print(f"Error Message: {str(error)}")


# ------------------------------------------------------------------------------------
def sqlite_get_data_custominput_rowsonly(database, sql_script, data_input):
    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]
    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?', data_input)
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as error:
        print(f"Error Message: {str(error)}")