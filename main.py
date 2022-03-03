from typing import Union

import aiohttp
import asyncio

import os
import logging
import config

from utils.compares import file_compares, get_msg_from_diff
from utils.json_files import JsonFile
from utils.orioks import get_student_info
from utils.yandex_disk import YandexDisk
from utils.send_message.main import SendMessage
from utils.get_current_time import get_current_time


async def logs_info_update(msg: str, send_notify: bool = False) -> None:
    logging.info(msg)
    if send_notify:
        await SendMessage.services(msg)

    filename = 'monitoring.log'
    await YandexDisk.download(filename=filename)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{get_current_time()}: {msg}\n")
    await YandexDisk.upload(filename=filename)
    os.remove(filename)


async def upload_diff(detailed_old_info, detailed_new_info, student_id: int) -> None:
    new_file = f'student_{student_id}_tmp_json_file_new.json'
    JsonFile.save(data=detailed_new_info, filename=new_file)
    JsonFile.save(data=detailed_old_info, filename='old_json.json')
    os.system(f'diff old_json.json {new_file} > diff_{student_id}.txt')
    os.remove(new_file)
    os.remove('old_json.json')
    with open(f'diff_{student_id}.txt', 'r') as file:
        diff_lines = file.read()
    os.remove(f'diff_{student_id}.txt')
    await logs_info_update(msg=f'diff: "{diff_lines}"', send_notify=False)


async def checker():
    student_id, detailed_info = await get_student_info()
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(id=student_id)

    await YandexDisk.download(filename=student_json_file)
    if student_json_file not in os.listdir(config.BASEDIR):
        await logs_info_update(msg=f'Создание нового файла данных... Скрипт запущен впервые?', send_notify=True)
        JsonFile.save(data=detailed_info, filename=student_json_file)
        await YandexDisk.upload(filename=student_json_file)
        return await checker()
    
    old_json = JsonFile.open(filename=student_json_file)
    diffs, errno = file_compares(old_file=old_json, new_file=detailed_info)
    if errno == 'Error':
        JsonFile.save(data=detailed_info, filename=student_json_file)
        await YandexDisk.upload(filename=student_json_file)
        await logs_info_update(msg=f'Структура файла данных поменялась. Начался новый семестр?', send_notify=True)
        await upload_diff(detailed_old_info=old_json, detailed_new_info=detailed_info, student_id=student_id)
        os.remove(student_json_file)
        return await checker()

    if len(diffs) > 0:
        msg = get_msg_from_diff(diffs)
        await logs_info_update(msg=msg, send_notify=True)

        JsonFile.save(data=detailed_info, filename=student_json_file)
        await YandexDisk.upload(filename=student_json_file)
    else:
        await logs_info_update(msg='Изменений нет.', send_notify=False)
        os.remove(student_json_file)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s: %(message)s',
        datefmt='%H:%M:%S %d.%m.%Y',
        level=logging.INFO,
    )
    asyncio.run(checker())
