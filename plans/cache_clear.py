import asyncio
import os

import schedule
import yaml
from loguru import logger

import pywxdll
from utils.plans_interface import PlansInterface


class cache_clear(PlansInterface):
    def __init__(self):
        main_config_path = "main_config.yml"
        with open(main_config_path, "r", encoding="utf-8") as f:  # 读取设置
            main_config = yaml.safe_load(f.read())

        self.ip = main_config["ip"]  # 机器人ip
        self.port = main_config["port"]  # 机器人端口
        self.timezone = main_config["timezone"]  # 时区
        self.bot = pywxdll.Pywxdll(self.ip, self.port)  # 机器人api

    async def job(self):
        path = "resources/cache/"  # 图片缓存路径
        for filename in os.listdir(path):  # 遍历文件夹
            file_path = os.path.join(path, filename)  # 获取文件路径
            # 判断路径是否为文件
            if os.path.isfile(file_path):  # 如果是文件
                # 删除文件
                os.remove(file_path)
        logger.info("[计划]清除缓存成功")  # 记录日志

    def job_async(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.job())

    def run(self):
        schedule.every(6).hours.do(self.job_async)  # 每六小时执行一次