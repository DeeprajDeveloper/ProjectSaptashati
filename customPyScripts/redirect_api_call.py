import customPyScripts.constants as const
import customPyScripts.project_utilities as utils


def redirect_fetch_verse_by_id(json_data_body):
    verse_id = json_data_body.get('verseId')
    verse_type = json_data_body.get('verseType')
    is_valid = False
    shloka_result_set = None
    if verse_id is None or (verse_type is None or verse_type == ''):
        is_valid = False
        shloka_json = [
            {'status': 'error', 'errorMessage': 'Mandatory fields missing.',
             'missingFields': [{'fieldName': 'verseId', 'acceptableValues': 'Number value that\'s determined based on verseType'}, {'fieldName': 'verseType', 'acceptableValues': 'introduction or chapters or conclusion'}]},
            404
        ]
    else:
        if verse_type == 'introduction':
            is_valid = True
            shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_INTRO_SHLOKA_BY_ID, data_input=verse_id)
        elif verse_type == 'chapters' or verse_type == 'chapter':
            is_valid = True
            shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTERS_SHLOKA_BY_ID, data_input=verse_id)
        elif verse_type == 'conclusion':
            is_valid = True
            shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_EXIT_SHLOKA_BY_ID, data_input=verse_id)
        else:
            is_valid = False

        if is_valid:
            shloka_json = utils.return_verse_json(result_set=shloka_result_set, verse_type=verse_type, verse_id=verse_id, name='')
        else:
            shloka_json = {
                'status': 'error', 'errorMessage': 'Invalid input received',
                'validTypeValues': {'fieldName': 'verseType', 'acceptableValues': 'introduction or chapters or conclusion'}
            }

    return shloka_json


def redirect_fetch_verse(json_data_body):
    try:
        verse_name = json_data_body.get('verseName').replace('\u200c', '')
        verse_type = json_data_body.get('verseType')
        shloka_result_set = []
        utils.log_message("info", f"(1) API Call Received for {verse_name}. Processing JSON input for Further processing.", call_type='API ')
        if verse_type == 'introduction':
            shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_SHLOKA, data_input=verse_name)
        elif verse_type == 'chapters' or verse_type == 'chapter':
            shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTERS_SHLOKA, data_input=verse_name)
        elif verse_type == 'conclusion':
            shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_SHLOKA, data_input=verse_name)
        shloka_json = utils.return_verse_json(result_set=shloka_result_set, verse_type=verse_type, verse_id='', name=verse_name)
        utils.log_message("info", f"(2) API Call Processed. Returning JSON response for Further processing.", call_type='API ')
        return shloka_json
    except Exception as err:
        utils.log_message("error", f"(x) {str(err)}", call_type='API ')
        return None
