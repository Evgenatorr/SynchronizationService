"""
Модуль запуска и обработки программы по синхронизации файлов
"""

import logging
import os
from time import sleep

import requests

import get_config
from api.api_ya_disk import ApiYandexDisk


def start_sync_file() -> None:
    """
    Функция запуска цикла синхронизации файлов
    """

    pc_dir: str = os.path.join(os.path.abspath(os.sep), get_config.path_sync_folder)
    serv_dir: str = get_config.dir_cloud_serv
    token: str = get_config.token
    sync_interval: str = get_config.sync_interval
    path_log_file = get_config.path_log_file
    sync = ApiYandexDisk(token, serv_dir)

    while True:
        sync_service(sync, serv_dir, pc_dir, path_log_file)
        sleep(int(sync_interval))


def sync_service(cls_sync, serv_dir, pc_dir, log_file) -> None:
    """
    Функция синхронизации файлов

    :param cls_sync: экземпляр класса синхронизации файлов
    :param serv_dir: директория яндекс диска
    :param pc_dir: отслеживаемая директория на системе пользователя
    :param log_file: путь к файлу логирования
    """

    logging.basicConfig(
        level=logging.INFO,
        filename=log_file,
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s (Функция: %(funcName)s)",
        encoding="utf-8",
    )

    try:
        files_serv_dir: dict[str, float] = cls_sync.get_info(serv_dir)

        for i_file in os.listdir(pc_dir):
            path_file: str = os.path.join(
                os.path.abspath(os.sep), get_config.path_sync_folder, i_file
            )

            time_ya_disk: float = files_serv_dir.get(i_file)
            time_file_pc: float = os.path.getmtime(path_file)

            if i_file not in files_serv_dir:
                with open(path_file, mode="rb") as file:
                    cls_sync.load(serv_dir, file)

                logging.info("Файл %s успешно записан", i_file)

            if i_file in files_serv_dir and time_file_pc > time_ya_disk:
                with open(path_file, mode="rb") as file:
                    cls_sync.reload(serv_dir, file)

                logging.info("Файл %s успешно перезаписан", i_file)

        for i_file in files_serv_dir.keys():
            if i_file not in os.listdir(pc_dir):
                cls_sync.delete(i_file)

                logging.info("Файл %s удален", i_file)

    except requests.exceptions.ConnectionError:
        logging.error(msg="Ошибка соединения")

    except (FileNotFoundError, AttributeError, PermissionError) as exc:
        logging.error(msg=exc)


if __name__ == "__main__":
    start_sync_file()
