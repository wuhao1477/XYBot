import os
import yaml
from loguru import logger
from wcferry import client
from utils.plugin_interface import PluginInterface
from wcferry_helper import XYBotWxMsg

class message_forward(PluginInterface):
    def __init__(self):
        super().__init__()
        config_path = os.path.join(os.path.dirname(__file__), "forward_config.yml")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.forward_rules = self.config.get("forward_rules", [])
        
    async def run(self, bot: client.Wcf, recv:XYBotWxMsg):
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
                                bot.send_image(recv.image, target)
                            elif recv.type == 34:  # 语音消息
                                bot.send_file(recv.voice, target)
                            # 可以添加其他类型的消息处理
                            logger.debug(f"消息已从群 {recv.roomid} 转发至群 {target}")
                        except Exception as e:
                            logger.error(f"转发消息失败: {e}")
        
        return forwarded  # 返回是否进行了转发