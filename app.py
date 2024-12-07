from flask import Flask, render_template, request
from customPyScripts import constants as const
import customPyScripts.project_utilities as utils
from datetime import datetime
import os

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', version=const.VERSION)


@app.route('/gettingStarted')
def getting_started():
    return render_template('01GettingStarted.html', version=const.VERSION)


@app.route('/initPurifyVerse')
def initial_purify_verses():
    # db_filepath = os.path.realpath(const.DATABASE_FILE)
    verses_list = utils.sqlite_retrieve_data(database=const.DATABASE_FILE, sql_script=const.SQL__GET_VERSE_LIST)
    return render_template('02InitiationPurification.html', optionList = verses_list, version=const.VERSION)


@app.route('/saptashatiVerses')
def saptashati_verses():
    # db_filepath = os.path.realpath(const.DATABASE_FILE)
    verses_list = utils.sqlite_retrieve_data(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTERS_LIST)
    return render_template('03ChandiPathChapters.html', optionList = verses_list, version=const.VERSION)


@app.route('/concludingVerses')
def concluding_verses():
    # db_filepath = os.path.realpath(const.DATABASE_FILE)
    verses_list = utils.sqlite_retrieve_data(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CONCLUDING_LIST)
    return render_template('04ConcludingVerses.html', optionList = verses_list, version=const.VERSION)


@app.route('/randomVerses')
def random_verses():
    # db_filepath = os.path.realpath(const.DATABASE_FILE)
    verses_list = utils.sqlite_retrieve_data(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CONCLUDING_LIST)
    return render_template('05RandomVerse.html', optionList = verses_list, version=const.VERSION)


@app.route('/purpose')
def purpose():
    current_year = datetime.now().year
    current_month = datetime.now().month
    year_diff = current_year - const.JOB_START_YEAR
    # month_diff = current_month = const.JOB_START_MONTH
    return render_template('06PurposeOfProject.html', version=const.VERSION, year=year_diff)


@app.route('/otherVerses')
def other_verses():
    return render_template('99UnderConstruction.html', version=const.VERSION)


# --------------------------------------------------------------------------------------
@app.route('/fetchVerse', methods=['POST'])
def fetch_verse():
    json_data_body = request.get_json()
    verse_name = json_data_body.get('verseName').replace('\u200c', '')
    verse_type = json_data_body.get('verseType')
    shloka_result_set = []

    if verse_type == 'introduction':
        shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_SHLOKA, data_input=verse_name)
    elif verse_type == 'chapters' or verse_type == 'chapter':
        shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTERS_SHLOKA, data_input=verse_name)
    elif verse_type == 'conclusion':
        shloka_result_set = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_SHLOKA, data_input=verse_name)
    shloka_json = return_verse_json(result_set=shloka_result_set, verse_type=verse_type, verse_id='', name=verse_name)
    # print(shloka_json)
    return shloka_json


# --------------------------------------------------------------------------------------
@app.route('/fetchVerseByID', methods=['POST'])
def fetch_verse_by_id():
    json_data_body = request.get_json()
    verse_id = json_data_body.get('verseId')
    verse_type = json_data_body.get('verseType')
    shloka_result_set = None
    is_valid = False
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
            shloka_json = return_verse_json(result_set=shloka_result_set, verse_type=verse_type, verse_id=verse_id, name='')
        else:
            shloka_json = {
                'status': 'error', 'errorMessage': 'Invalid input received',
                'validTypeValues': {'fieldName': 'verseType', 'acceptableValues': 'introduction or chapters or conclusion'}
            }

    return shloka_json


def return_verse_json(result_set, verse_type, verse_id, name):
    data_list = []
    latin_translation = []
    additional_context = {}
    meanings = ['', '']
    if result_set is not None:
        for item in result_set:
            if verse_type == 'introduction':
                latin_translation = utils.sqlite_get_data_custominput_rowsonly(database=const.DATABASE_FILE, sql_script=const.SQL__GET_TRANSLATION_INTRO_EXIT, data_input=str(item[2]))
                meanings = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_MEANING_INTRO_EXIT, data_input=str(item[2]))[0]
                if verse_id == '':
                    storta_name = name
                else:
                    intro_details = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_STOTRA_NAME, data_input=str(verse_id))[0]
                    storta_name = intro_details[0] if (intro_details[1] is None or intro_details[1] == "") else f"{intro_details[0]} - {intro_details[1]}"
                additional_context = {'stortaName': storta_name}
            elif verse_type == 'chapters' or verse_type == 'chapter':
                latin_translation = utils.sqlite_get_data_custominput_rowsonly(database=const.DATABASE_FILE, sql_script=const.SQL__GET_TRANSLATION_CHAPTERS, data_input=str(item[2]))
                if verse_id == '':
                    additional_context = {'chapterName': name}
                else:
                    chapter_details = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTER_NAME, data_input=str(verse_id))[0]
                    additional_context = {'chapterName': chapter_details[0], 'charitraName': chapter_details[1]}
            elif verse_type == 'conclusion':
                latin_translation = utils.sqlite_get_data_custominput_rowsonly(database=const.DATABASE_FILE, sql_script=const.SQL__GET_TRANSLATION_INTRO_EXIT, data_input=str(item[2]))

            item_json = {
                'id': item[2],
                'verseNo': item[1] if item[1] is not None else '',
                'devanagariShloka': item[0],
                'latinTranslation': latin_translation[0],
                'meanings': {'englishMeaning': meanings[0], 'hindiMeaning': meanings[1]},
                'additionalContext': additional_context
            }

            data_list.append(item_json)
        if len(data_list) == 0:
            data_values = []
            if verse_type == 'introduction':
                data_values = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_INTRO_MIN_MAX, data_input='')
            elif verse_type == 'chapters' or verse_type == 'chapter':
                data_values = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTERS_MIN_MAX, data_input='')
            elif verse_type == 'conclusion':
                data_values = utils.sqlite_retrieve_data_custominput(database=const.DATABASE_FILE, sql_script=const.SQL__GET_EXIT_MIN_MAX, data_input='')
            data_list = {'status': 'error', 'errorMessage': 'No data available', 'acceptableValues': f'Verse ID must be between {data_values[0]} for {verse_type}'}
    return data_list


if __name__ == '__main__':
    print('[INFO] Application is running')
    app.run(debug=True, port=700)
