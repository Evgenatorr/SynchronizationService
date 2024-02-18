import unittest
import get_config
from api.api_ya_disk import ApiYandexDisk
import os
from main import start_sync_file


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pc_dir: str = os.path.join(os.path.abspath(os.sep), get_config.path_sync_folder)
        cls.serv_dir: str = get_config.dir_cloud_serv
        cls.token: str = get_config.token
        cls.sync_interval: str = get_config.sync_interval
        cls.path_log_file: str = get_config.path_log_file
        cls.file_name: str = 'test_file.txt'

    def test_start_sync_file(self):
        start_sync_file()
        my_file = open(self.file_name, "w+")


if __name__ == "__main__":
    unittest.main()
