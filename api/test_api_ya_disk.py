import unittest
from api_ya_disk import ApiYandexDisk
import get_config


class TestApiYandexDisk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.headers: dict[str, str] = {"Authorization": get_config.token}
        cls.serb_dir = get_config.dir_cloud_serv

    def test_get_info(self):

        self.fail()

    def test_load(self):
        self.fail()

    def test_reload(self):
        self.fail()

    def test_delete(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
