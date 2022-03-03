import os


ORIOKS_LOGPASS = {
    'login': os.getenv("ORIOKS_LOGPASS_LOGIN"),
    'password': os.getenv("ORIOKS_LOGPASS_PASSWORD"),
}

YANDEX_DISK = {
    'Authorization': f'OAuth {os.getenv("YANDEX_DISK_API_TOKEN")}',
}

VK = {
    'api_version': 5.111,
    'access_token': os.getenv("VK_API_TOKEN"),
    'peer_id': os.getenv("VK_PEER_ID"),
    'use': os.getenv("VK_USE"),
}

TG = {
    'access_token': os.getenv("TG_API_TOKEN"),
    'chat_id': os.getenv("TG_CHAT_ID"),
    'use': os.getenv("TG_USE"),
}

STUDENT_FILE_JSON_MASK = 'student_{id}.json'

BASEDIR = os.path.dirname(os.path.abspath(__file__))
