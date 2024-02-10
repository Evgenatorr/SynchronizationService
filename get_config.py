"""
Модуль получения параметров для работы программы
"""

import configparser
from configparser import ConfigParser

config: ConfigParser = configparser.ConfigParser()
config.read('config.ini')

try:

    path_sync_folder: str = config.get('settings', 'path_sync_folder')
    dir_cloud_serv: str = config.get('settings', 'dir_cloud_serv')
    token: str = config.get('settings', 'token')
    sync_interval: str = config.get('settings', 'sync_interval')
    path_log_file: str = config.get('settings', 'path_log_file')

except configparser.NoOptionError as exc:
    print(exc)

else:
    print('Переменные окружения успешно загружены.')
