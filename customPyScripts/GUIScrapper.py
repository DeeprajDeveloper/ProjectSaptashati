import customPyScripts.project_utilities as utils
import constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

url = r'https://www.lexilogos.com/keyboard/sanskrit_conversion.htm'
# select_script = r"select d.chapterVerse, d.rowID from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.name like '?%' or s.classification like '?%' and d.ssmid <> 89 order by d.rowID asc"
# select_script = r"select d.completeVerse, d.vrID from stotraSuktaMantraInfo s inner join deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.name like '?%' order by d.vrID asc"
database_file = r'../database/deviSaptashatiDB.db'

driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()

query_list = []

verse_name_list = utils.sqlite_retrieve_data(database_file, const.SQL__GET_CONCLUDING_LIST)
for verse_name in verse_name_list:
    print(f'Converting shloka from {verse_name}')
    verses_list = utils.sqlite_retrieve_data_custominput(database_file, select_script, verse_name)
    for shloka in verses_list:
        try:
            devanagari_input = driver.find_element(By.ID, 'bar1')
            devanagari_input.send_keys(shloka[0])
            time.sleep(0.5)
            latin_output = driver.find_element(By.ID, 'bar2')
            translated_text = latin_output.get_attribute("value")
            insert_statement = f"INSERT INTO shlokaTransLiterationMeaning (rowID, latinTranslation) values ({shloka[1]}, '{translated_text}')"
            query_list.append(insert_statement)
            devanagari_input.clear()
            latin_output.clear()
            utils.sqlite_execute_script(database_file, insert_statement)
            print(f"\tVerse Converted - {shloka[1]}")
        except Exception as error:
            print(str(error))

print('---------------------------------')
print(query_list)



# verses_list = utils.sqlite_retrieve_data_custominput(database=database_file, sql_script=select_script, data_input='')
# for shloka in verses_list:
#     try:
#         print(shloka)
#         devanagari_input = driver.find_element(By.ID, 'bar1')
#         devanagari_input.send_keys(shloka[0])
#         time.sleep(0.5)
#         latin_output = driver.find_element(By.ID, 'bar2')
#         translated_text = latin_output.get_attribute("value")
#         insert_statement = f"INSERT INTO shlokaTransLiterationMeaning (rowID, latinTranslation) values ({shloka[1]}, '{translated_text}')"
#         query_list.append(insert_statement)
#         devanagari_input.clear()
#         latin_output.clear()
#         utils.sqlite_execute_script(database_file, insert_statement)
#         print(f"\tVerse Converted - {shloka}")
#     except Exception as error:
#         print(str(error))
#
# print('---------------------------------')
# print(query_list)