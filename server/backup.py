import os
import subprocess
from datetime import date

import requests

from config.config import get_custom_config
from logger import create_logger, BACKUP_LOGGER_NAME, create_smtp_handler

LOG = None
BACKUP_LOG_FILE = 'backup.log'
config = None
backup_file_path = ''
backup_file_name = ''
BACKUP_MAX_FILES = 5


class _MysqlDumpError(Exception):
    pass


class YandexDiskError(Exception):
    code = None

    def __init__(self, code, text):
        super(YandexDiskError, self).__init__(text)
        self.code = code

    def __str__(self):
        return '%d. %s' % (self.code, super(YandexDiskError, self).__str__())


class YandexDiskRestClient:
    _base_url = 'https://cloud-api.yandex.net:443/v1/disk'

    def __init__(self, token):
        self.token = token

        self.base_headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }

    def list_files(self, path_to_folder):
        url = self._base_url + '/resources'
        payload = {'path': path_to_folder}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        files = []
        if '_embedded' in json_dict:
            for item in json_dict['_embedded']['items']:
                if item['type'] == 'file':
                    files.append(item['path'])
        return files

    def remove_file(self, path):
        url = self._base_url + '/resources'
        payload = {'path': path}
        r = requests.delete(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def upload_file(self, path_from, path_to):
        url = self._base_url + '/resources/upload'
        payload = {'path': path_to}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        upload_link = json_dict['href']

        with open(path_from, 'rb') as fh:
            files = {'file': fh}
            r2 = requests.put(upload_link, headers=self.base_headers, files=files)
            self._check_code(r2)

    @staticmethod
    def _check_code(req):
        if not str(req.status_code).startswith('2'):
            raise YandexDiskError(req.status_code, req.text)


def _create_backup():
    global backup_file_path, backup_file_name
    today = date.today()
    backup_file_name = '{}_{}.sql.gz'.format(config.DB_NAME, today.strftime('%Y%m%d'))
    backup_file_path = '{}/{}'.format(config.BACKUP_DIR, backup_file_name)
    cmd = 'mysqldump -u {} -p{} {} | gzip > {}'.format(config.DB_USER, config.DB_PASSWORD, config.DB_NAME,
                                                       backup_file_path)
    subprocess.run(cmd, shell=True, check=True)
    if os.stat(backup_file_path).st_size < 50:
        # If mysqldump returns error, it is pipelined to gzip and it results in tiny backup file(~20 bytes)
        LOG.error('mysqldump fails')
        raise _MysqlDumpError
    LOG.info('Backup created')


def _remove_backup():
    # Remove local backup file
    if os.path.isfile(backup_file_path):
        os.remove(backup_file_path)
        LOG.info('Backup removed')


def _upload_backup():
    cl = YandexDiskRestClient(config.YANDEX_API_TOKEN)
    cl.upload_file(backup_file_path, 'app:/{}'.format(backup_file_name))
    LOG.info('Backup uploaded')


def _remove_old_backups():
    # Remove old files from Yandex Disk
    cl = YandexDiskRestClient(config.YANDEX_API_TOKEN)
    files_to_remove = sorted(cl.list_files('app:/'))[:-BACKUP_MAX_FILES]
    for f in files_to_remove:
        cl.remove_file(f)
    LOG.info('Backup cleanup')


def main():
    LOG.info('Backup start')
    try:
        _create_backup()
        _upload_backup()
        _remove_old_backups()
    except _MysqlDumpError:
        pass
    except Exception:
        LOG.exception('Exception during backup')
    finally:
        _remove_backup()
    LOG.info('Backup end')


if __name__ == '__main__':
    config = get_custom_config()
    email_handler = create_smtp_handler(config, 'Backup:Error')
    LOG = create_logger(BACKUP_LOGGER_NAME, config.LOG_DIR + BACKUP_LOG_FILE, email_handler=email_handler)
    main()
