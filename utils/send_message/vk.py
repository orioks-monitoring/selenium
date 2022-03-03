import aiohttp
import asyncio

import random
import config


async def send_message(msg: str) -> None:
    url = f"https://api.vk.com/method/messages.send?v={config.VK['api_version']}&access_token={config.VK['access_token']}&peer_id={config.VK['peer_id']}&random_id={random.randint(0, 21474836)}&message={msg}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                print("ERROR (send_message)")
