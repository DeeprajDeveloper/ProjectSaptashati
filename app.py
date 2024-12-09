from flask import Flask, render_template, request
from customPyScripts import constants as const
import customPyScripts.project_utilities as utils
import customPyScripts.redirect_api_call as api
from datetime import datetime
import logging

app = Flask(__name__)
app.json.sort_keys = False
# Suppress Flask's default logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
@app.route('/home')
def index():
    """ Loading Home Page """
    utils.log_message("info", "Loading index.html page", call_type='GUI ')
    return render_template('index.html', version=const.VERSION)


@app.route('/gettingStarted')
def getting_started():
    """ Getting Started Page """
    utils.log_message("info", "Loading 01GettingStarted.html", call_type='GUI ')
    return render_template('01GettingStarted.html', version=const.VERSION)


@app.route('/initPurifyVerse')
def initial_purify_verses():
    """ Loading "Step 1: Initiation and Purification Verses" page """
    utils.log_message("info", "Loading 02InitiationPurification.html", call_type='GUI ')
    verses_list = utils.sqlite_retrieve_data(database=const.DATABASE_FILE, sql_script=const.SQL__GET_VERSE_LIST)
    return render_template('02InitiationPurification.html', optionList=verses_list, version=const.VERSION)


@app.route('/saptashatiVerses')
def saptashati_verses():
    """ Loading "Step 2: Chandi/Saptashati Path" page """
    utils.log_message("info", "Loading 03ChandiPathChapters.html", call_type='GUI ')
    verses_list = utils.sqlite_retrieve_data(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CHAPTERS_LIST)
    return render_template('03ChandiPathChapters.html', optionList=verses_list, version=const.VERSION)


@app.route('/concludingVerses')
def concluding_verses():
    """ Loading "Step 3: Conclusion Verses" page """
    utils.log_message("info", "Loading 04ConcludingVerses.html", call_type='GUI ')
    verses_list = utils.sqlite_retrieve_data(database=const.DATABASE_FILE, sql_script=const.SQL__GET_CONCLUDING_LIST)
    return render_template('04ConcludingVerses.html', optionList=verses_list, version=const.VERSION)


@app.route('/purpose')
def purpose():
    """ Loading "About the Website" page """
    current_year = datetime.now().year
    year_diff = current_year - const.JOB_START_YEAR
    utils.log_message("info", "Loading 06PurposeOfProject.html", call_type='GUI ')
    return render_template('06PurposeOfProject.html', version=const.VERSION, year=year_diff)


@app.route('/otherVerses')
def other_verses():
    """ Loading "Other Verses" page """
    utils.log_message("info", "Loading 99UnderConstruction.html", call_type='GUI ')
    return render_template('99UnderConstruction.html', version=const.VERSION)


# -------------------------------------------------------------------------------------
# API Calls
@app.route('/fetchVerse', methods=['POST'])
def fetch_verse():
    utils.log_message("info", "(1) App received API Call with JSON request.", call_type='APP ')
    shloka_json = api.redirect_fetch_verse(json_data_body=request.get_json())
    utils.log_message("info", "(2) App sending API response.", call_type='APP ')
    return shloka_json


# --------------------------------------------------------------------------------------
@app.route('/fetchVerseByID', methods=['POST'])
def fetch_verse_by_id():
    utils.log_message("info", "API Call Initiated.", call_type='API ')
    shloka_json = api.redirect_fetch_verse_by_id(json_data_body=request.get_json())
    utils.log_message("info", "API Call Completed.", call_type='API ')
    return shloka_json


# -------------------------------------------------------------------------------------
# API Calls
@app.route('/v1/fetchAllVerse', methods=['GET'])
def fetch_all_verses():
    shloka_json = None
    try:
        utils.log_message("info", "(1) API Call Initiated.", call_type='API')
        shloka_json = api.redirect_fetch_verse(json_data_body=request.get_json())
        utils.log_message("info", "(2) API Call Complete.", call_type='API')
    except Exception as err:
        utils.log_message("error", str(err), call_type='API')
    return shloka_json


if __name__ == '__main__':
    print('-------------------------------------')
    print('[app.py][INFO] Application is running')
    app.run(debug=True, port=700)
    print('-------------------------------------')
