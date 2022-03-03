#!/bin/bash


curl -X PUT -H "Authorization: OAuth ${YANDEX_DISK_API_TOKEN}" "https://cloud-api.yandex.net/v1/disk/resources?path=app:/orioks_monitoring_selenium/"
