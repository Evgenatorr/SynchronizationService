"""
Модуль с классом синхронизации файлов
"""

import logging
import os
from datetime import datetime

import requests
from requests import Response


def file_url_upload(
    path: str, file_name: str, headers: dict[str, str], overwrite=None
) -> str:
    """
    Вспомогательная функция возвращающая ссылку для загрузки файла на облачное хранилище
    :param path: директория на облачном сервисе куда сохраняются файлы
    :param file_name: имя файла, который нужно загрузить на сервис
    :param headers: headers api
    :param overwrite: отвечает за перезапись файла на сервис
    :return: Ссылка для загрузки файла на облачное хранилище
    """

    if overwrite is True:
        params: dict[str, bool] = {"overwrite": True}
    else:
        params: None = None

    base_url: str = (
        f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={path}/{file_name}"
    )
    try:
        response: Response = requests.get(
            base_url, headers=headers, params=params, timeout=10
        )

        if response.status_code != 200:
            logging.info('Не удалось выполнить "requests" запрос')

        json_response: dict = response.json()
        return json_response["href"]

    except KeyError as exc:
        logging.error(msg=exc)


class ApiYandexDisk:
    """
    Класс синхронизации файлов
    """

    def __init__(self, token, serv_dir):
        self.headers: dict[str, str] = {"Authorization": token}
        self.serv_dir: str = serv_dir

    def get_info(self, path) -> dict[str, float]:
        """
        Метод получение информации о файлах на сервисе облачного хранилища
        :param path: директория на облачном сервисе куда сохраняются файлы
        :return: словарь с файлами
        """

        base_url: str = f"https://cloud-api.yandex.net/v1/disk/resources?path={path}"
        params: dict[str, str] = {
            "fields": "_embedded.items.name,_embedded.items.modified"
        }
        try:
            response: Response = requests.get(
                base_url, headers=self.headers, params=params, timeout=10
            )

            if response.status_code != 200:
                logging.info('Не удалось выполнить "requests" запрос')

            json_response: dict = response.json()
            result: dict[str, float] = {
                elem["name"]: datetime.fromisoformat(elem["modified"]).timestamp()
                for elem in json_response["_embedded"]["items"]
            }

            return result

        except KeyError as exc:
            logging.error(msg=exc)

    def load(self, path, file, overwrite=None) -> None:
        """
        Метод загрузки файла на облачное хранилище
        :param path: директория на облачном сервисе куда сохраняются файлы
        :param file: файл открытый в бинарном режиме только для чтения
        :param overwrite: отвечает за перезапись файла на сервис
        """

        file_name: str = os.path.basename(f"{file.name}")

        if overwrite:
            url_upload: str = file_url_upload(path, file_name, self.headers, overwrite)
        else:
            url_upload: str = file_url_upload(path, file_name, self.headers)

        response = requests.put(url_upload, files={"file": file}, timeout=10)

        if response.status_code != 201:
            logging.info('Не удалось выполнить "requests" запрос')

    def reload(self, path, file) -> None:
        """
        Функция для перезаписи файла
        :param path: директория на облачном сервисе куда сохраняются файлы
        :param file: файл открытый в бинарном режиме только для чтения
        """

        self.load(path, file, overwrite=True)

    def delete(self, filename) -> None:
        """
        Функция для удаления файла с директории на сервисе облачного хранилища
        :param filename: имя файла, который нужно удалить
        """

        base_url: str = f"https://cloud-api.yandex.net/v1/disk/resources?path={self.serv_dir}/{filename}"
        response = requests.delete(base_url, headers=self.headers, timeout=10)

        if response.status_code != 204:
            logging.info('Не удалось выполнить "requests" запрос')
