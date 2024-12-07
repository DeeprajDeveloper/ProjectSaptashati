# Application version
VERSION = 'v20241123.1.0.0'

# Database Connection String
DATABASE_FILE = r'.\database\deviSaptashatiDB.db'

# Get list of verse Names to show them on the buttons
SQL__GET_VERSE_LIST = r"SELECT DISTINCT name FROM stotraSuktaMantraInfo WHERE whenToRead = 'Intro' ORDER BY orderId ASC"
SQL__GET_CHAPTERS_LIST = r"SELECT DISTINCT name FROM stotraSuktaMantraInfo WHERE whenToRead = 'Main' ORDER BY orderId ASC"
SQL__GET_CONCLUDING_LIST = r"SELECT DISTINCT name FROM stotraSuktaMantraInfo WHERE whenToRead = 'Exit' ORDER BY orderId ASC"

# Get the list of verses for each verse name
SQL__GET_SHLOKA = r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.name like '?%' ORDER BY d.vrID ASC"
SQL__GET_ALL_SHLOKA = r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId ORDER BY d.vrID ASC"
SQL__GET_CHAPTERS_SHLOKA = r"select d.chapterVerse, d.vrNo, d.rowID from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.name like '?%' or s.classification like '?%' order by d.rowID asc"

# Get english Transliteration in IAST format
SQL__GET_TRANSLATION_INTRO_EXIT = r"SELECT latinTranslation FROM shlokaTransLiterationMeaning where vrID = '?'"
SQL__GET_TRANSLATION_CHAPTERS = r"SELECT latinTranslation FROM chaptersShlokaTransLiterationMeaning where rowID = '?'"

# Get english Transliteration in IAST format
SQL__GET_MEANING_INTRO_EXIT = r"SELECT englishMeaning, devanagariMeaning FROM shlokaTransLiterationMeaning where vrID = '?'"
SQL__GET_MEANING_CHAPTERS = r"SELECT englishMeaning, devanagariMeaning FROM chaptersShlokaTransLiterationMeaning where rowID = '?'"

# Get the list of verses for each verse ID
SQL__GET_INTRO_SHLOKA_BY_ID = r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where d.vrID = ? and s.whenToRead = 'Intro' ORDER BY d.vrID ASC"
SQL__GET_EXIT_SHLOKA_BY_ID = r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where d.vrID = ? and s.whenToRead = 'Exit' ORDER BY d.vrID ASC"
SQL__GET_CHAPTERS_SHLOKA_BY_ID = r"select d.chapterVerse, d.vrNo, d.rowID from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.whenToRead = 'Main' and d.rowID = ? or s.classification like '?%' order by d.rowID asc"

# Get the list of verses for each verse ID
SQL__GET_INTRO_SHLOKA_ALL = r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Intro' ORDER BY d.vrID ASC"
SQL__GET_EXIT_SHLOKA_ALL = r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Exit' ORDER BY d.vrID ASC"
SQL__GET_CHAPTERS_SHLOKA_ALL = r"select d.chapterVerse, d.vrNo, d.rowID from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.whenToRead = 'Main' order by d.rowID asc"

# Get min-max values
SQL__GET_INTRO_MIN_MAX = r"SELECT MIN(d.vrID), MAX(d.vrID) FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Intro' ORDER BY d.vrID ASC"
SQL__GET_EXIT_MIN_MAX = r"SELECT MIN(d.vrID), MAX(d.vrID) FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Exit' ORDER BY d.vrID ASC"
SQL__GET_CHAPTERS_MIN_MAX = r"select MIN(d.rowID), MAX(d.rowID) from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.whenToRead = 'Main' order by d.rowID asc"

# Get Chapter details
SQL__GET_CHAPTER_NAME = r"select cni.chapterName, cni2.charitraName from stotraSuktaMantraInfo ssmi inner join deviSaptashatiChapters dsc on dsc.ssmID = ssmi.ssmId inner join chapterNameInfo cni on cni.chapterNo = dsc.chapterNo inner join charitraNameInfo cni2 on cni2.charitraNo = dsc.charitraNo where dsc.rowID in (?)"
SQL__GET_STOTRA_NAME = r"select ssmi.name, ssmi.classification from stotraSuktaMantraInfo ssmi inner join deviSaptashatiOtherVerses dsov on dsov.ssmID = ssmi.ssmId where dsov.vrID in (?)"

# Miscellaneous
JOB_START_YEAR = 2018
JOB_START_MONTH = 6
