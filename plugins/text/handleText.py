#  Copyright (c) 2024. Henry Yang
#
#  This program is licensed under the GNU General Public License v3.0.

from loguru import logger
from wcferry import client

from utils.plugin_interface import PluginInterface
from wcferry_helper import XYBotWxMsg


class handle_ext(PluginInterface):
    def __init__(self):
        pass

    async def run(self, bot: client.Wcf, recv: XYBotWxMsg):
        logger.info(f"[收到文本插件的消息]:{recv}")
