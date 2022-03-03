from typing import Union

import aiohttp
import asyncio
import aiofiles

import json
import os

import config


async def upload_to_ydisk(filename: str):
    headers = config.YANDEX_DISK
    url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path=app:/orioks_monitoring_selenium/{filename}&overwrite=true'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            ydisk_resp = await resp.json()

    if 'href' not in ydisk_resp:
        return None
    os.system(f"curl {ydisk_resp['href']} --upload-file {filename}")
    return 'OK'


async def download_from_ydisk(filename: str):
    headers = config.YANDEX_DISK
    url = f'https://cloud-api.yandex.net/v1/disk/resources/download?path=app:/orioks_monitoring_selenium/{filename}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            ydisk_resp = await resp.json()

        if 'href' not in ydisk_resp:
            return None

        async with session.get(ydisk_resp['href'], headers=headers) as resp:
            f = await aiofiles.open(filename, mode='wb')
            await f.write(await resp.read())
            await f.close()
    return 'OK'


class YandexDisk:
    @staticmethod
    async def upload(filename: str):
        return await upload_to_ydisk(filename=filename)


    @staticmethod
    async def download(filename: str):
        return await download_from_ydisk(filename=filename)
