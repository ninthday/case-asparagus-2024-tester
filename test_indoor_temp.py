#!/usr/bin/env python3

import configparser
import json
import math
from datetime import datetime
from pathlib import Path

import pytz

from agriweather.storage.asparagus_storage import AsparagusStorage


def to_radians(angle):
    return angle * (math.pi / 180)


def calculate_indoor_temperature(temperature, humidity, hour: int):
    factor = math.sin(to_radians((hour * 15) - 90))
    return 4.1218 + 0.9986 * temperature - 0.03417 * humidity + 2.36591 * factor


def trans_time(time_str):
    # 將字串解析為 datetime 對象（UTC 時間）
    utc_time = datetime.fromisoformat(time_str)

    # 定義 Taipei 時區
    taipei_tz = pytz.timezone("Asia/Taipei")

    # 將 UTC 時間轉換為 Taipei 時間
    taipei_time = utc_time.astimezone(taipei_tz)
    return taipei_time


if __name__ == "__main__":
    dir_path = Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read("{}/config.ini".format(dir_path))

    # if config.getboolean("SmeargleCfg", "Debug"):
    #     log_level = "DEBUG"
    # else:
    #     log_level = "INFO"
    try:
        storage = AsparagusStorage(
            config.get("RDB", "DB_HOST"),
            config.get("RDB", "DB_USERNAME"),
            config.get("RDB", "DB_PASSWORD"),
            config.get("RDB", "DB_DATABASE"),
            "/var/log/agriweather",
            "DEBUG",
        )
    except Exception as e:
        print(e)

    forecast = storage.get_forecast("09f9b7dd-8b00-42f8-a5c8-72c37adfd5d8")

    forecast_data = forecast["data"].replace("\\", "")
    forecast_data = forecast_data[1:-1]
    new_forecast_data = json.loads(forecast_data)
    # forecast_data = json.loads(forecast.get("data").replace("\\", ""))
    # forecast_data = forecast.get("data").replace("\\", "")

    indoor_temp = dict()

    for data in new_forecast_data:
        taipei_time = trans_time(data["forecast_time"]["end"])
        indoor_temp[data["forecast_time"]["end"]] = {
            "tw_time": taipei_time.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": taipei_time.hour,
            "temperature": data["tempture"],
            "humidity": data["rh"],
            "indoor_temp": calculate_indoor_temperature(
                data["tempture"], data["rh"], taipei_time.hour
            ),
        }

    # print(forecast_data)
    # print(type(forecast_data))
    print(new_forecast_data[0])
    print(type(new_forecast_data))

    print(json.dumps(indoor_temp, indent=4))
