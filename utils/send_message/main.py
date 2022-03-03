import config
import utils.send_message.tg as tg
import utils.send_message.vk as vk


def str2bool(string: str) -> bool:
    return string.lower() in ('yes', 'y', 'true', 't', '1', 'yeah', 'yup', 'certainly', 'uh-huh')


class SendMessage:
    async def __vk(msg: str) -> None:
        return await vk.send_message(msg)


    async def __tg(msg: str) -> None:
        return await tg.send_message(msg)

    @staticmethod
    async def services(msg: str) -> None:
        if str2bool(config.VK['use']):
            await SendMessage.__vk(msg)
        if str2bool(config.TG['use']):
            await SendMessage.__tg(msg)
