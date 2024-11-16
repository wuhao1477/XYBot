#  Copyright (c) 2024. Henry Yang
#
#  This program is licensed under the GNU General Public License v3.0.

from loguru import logger
from wcferry import client

from utils.plugin_interface import PluginInterface
from wcferry_helper import XYBotWxMsg


class image(PluginInterface):
    def __init__(self):
        pass

    async def run(self, bot: client.Wcf, recv: XYBotWxMsg):
        logger.debug(f"收到图片消息！{recv}")
        # bot.send_text(f"收到图片消息！", recv.roomid)
        # bot.send_image(recv.image, recv.roomid)
