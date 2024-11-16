import os
import yaml
from loguru import logger
from wcferry import client
from utils.plugin_interface import PluginInterface
from wcferry_helper import XYBotWxMsg, async_download_image, async_get_audio_msg, async_download_video

class message_forward(PluginInterface):
    def __init__(self):
        super().__init__()
        config_path = os.path.join(os.path.dirname(__file__), "forward_config.yml")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f) or {}  # 如果加载结果为None，使用空字典
        self.forward_rules = self.config.get("forward_rules", []) or []  # 如果forward_rules为None，使用空列表
        self.image_save_path = os.path.abspath("resources/cache")
        self.voice_save_path = os.path.abspath("resources/cache")
        logger.debug(f"语音保存路径: {self.voice_save_path}")
        logger.debug(f"图片保存路径: {self.image_save_path}")

    async def run(self, bot: client.Wcf, recv: XYBotWxMsg):
        forwarded = False
        # 检查消息来源是否在转发规则中
        for rule in self.forward_rules:
            source_groups = rule.get("from", [])
            target_groups = rule.get("to", [])

            if recv.roomid in source_groups:
                forwarded = True
                print(f"消息来源群 {recv.roomid} 在转发规则中")
                for target in target_groups:
                    if target != recv.roomid:  # 避免自循环转发
                        try:
                            if recv.type == 1:  # 文本消息
                                bot.send_text(recv.content, target)
                            elif recv.type == 3:  # 图片消息
                                # 如果是图片消息，recv字典中会有一个image键值对，值为图片的绝对路径。
                                path = await async_download_image(bot, recv.id, recv.extra, self.image_save_path)
                                recv.image = os.path.abspath(path)  # 确保图片为绝对路径
                                bot.send_image(recv.image, target)
                            elif recv.type == 34:  # 语音消息
                                path = await async_get_audio_msg(bot, recv.id, self.voice_save_path)  # 下载语音
                                recv.voice = os.path.abspath(path)  # 确保语音为绝对路径
                                bot.send_file(recv.voice, target)
                            # elif recv.type == 43:  # 视频消息
                            # 视频暂时不支持
                            #     print(recv)
                            #     path = await async_download_image(bot, recv.id, recv.extra, self.image_save_path, 300)  # 下载视频
                            #     recv.voice = os.path.abspath(path)  # 确保视频为绝对路径
                            #     bot.send_image(recv.voice, target)
                            # 可以添加其他类型的消息处理
                            else :
                                logger.warning(f"未知消息类型: {recv.type}，直接转发")
                                bot.forward_msg(recv.id, target)

                            logger.debug(f"消息已从群 {recv.roomid} 转发至群 {target}")
                        except Exception as e:
                            logger.error(f"转发消息失败: {e}")

        return forwarded  # 返回是否进行了转发