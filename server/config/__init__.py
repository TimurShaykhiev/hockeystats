# DB config
DB_NAME = 'NHL_STATS'
DB_URL = 'localhost'
DB_USER = 'hockstats'
DB_PASSWORD = 'hockstats'

# Logger settings
LOG_DIR = '/home/timur/hockeystats/log/'
HOCKEY_STATS_LOG_LEVEL = 'DEBUG'
FILTER_THROTTLING_INTERVAL = 60

# Email settings
EMAIL_TO_ADDR = 't.shaykhiev@yandex.ru'
EMAIL_FROM_ADDR = 'logger@hockstats.ru'
EMAIL_SMTP_ADDR = 'smtp.yandex.ru'
EMAIL_SMTP_PORT = 465
EMAIL_LOGIN = 'logger@hockstats.ru'
EMAIL_PASSWORD = ''

# Backup settings
BACKUP_DIR = '/home/timur/backup'
YANDEX_API_TOKEN = ''

# Flask
DEBUG = True
LOGGER_NAME = 'hockeystats'
