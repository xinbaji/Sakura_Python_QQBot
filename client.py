import botpy
import asyncio
import os
from botpy.message import Message,DirectMessage
from botpy import logging
import json

with open ("config.json","r") as f:
    test_config=json.load(f)
    f.close()

_log = logging.get_logger()


class SakuraClient(botpy.Client):
    
    async def on_ready(self):
        self.url_list=[]
        self.recv_email=""
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_direct_message_create(self, message: DirectMessage):
        '''await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"机器人{self.robot.name}收到你的私信了: {message.content}",
                msg_id=message.id,
            )'''
        if "/下载学科网" in message.content:
            with open ("C:\\Users\\40751\\Desktop\\Xkw_AutoDownloader\\tasks\\status.json","r") as f:
                status=json.load(f)
                f.close()
            if status == "done":
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    content=f"{self.robot.name}准备好下载了，首先输入 /qqemail +(接收者的邮箱qq号)~",
                    msg_id=message.id,
                    )
            elif status == "busy":
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    content=f"活还没干完呢~ 主人可以喝杯茶等一下哦~",
                    msg_id=message.id,
                    )
            
        elif "/qqemail" in message.content:
            mc=message.content
            mc=mc.replace("/qqemail","").replace(" ","")
            self.recv_email=mc+"@qq.com"
            _log.info(f"robot 「{self.robot.name}」 接收者邮箱为： "+self.recv_email)
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"已确认课件发送至Q邮： "+mc+",接下来输入 /xkwid +(课件的链接中的课件id) ,输入ok结束输入~",
                msg_id=message.id,
            )
        elif "/xkwid" in message.content:
            mc1=message.content
            mc1=mc1.replace("/xkwid","").replace(" ","")
            url="https://www.zxxk.com/soft/"+mc1+".html"
            self.url_list.append(url)
            _log.info(f"robot 「{self.robot.name}」 已添加资料链接至队列： "+url)
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"已添加资料id: "+str(mc1)+",输入ok结束输入~",
                msg_id=message.id,
            )
            
        elif "ok" in message.content:
            if self.recv_email != "" and len(self.url_list) != 0:
                dic={
                    "recv_email":self.recv_email,
                    "task":self.url_list
                }
                with open ("C:\\Users\\40751\\Desktop\\Xkw_AutoDownloader\\tasks\\task.json","w") as f:
                    json.dump(dic,f)
                    f.close()
                _log.info(f"robot 「{self.robot.name}」 开始提交任务队列至服务器")    
                await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"主人~我已生成任务队列，正在下载中~",
                msg_id=message.id,
                )
                
                self.recv_email=""
                self.url_list=[]
            else:
                await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"主人~你还没有写参数哦，杂鱼~",
                msg_id=message.id,
                )
        
        elif "/status" in message.content:
            with open ("C:\\Users\\40751\\Desktop\\Xkw_AutoDownloader\\tasks\\status.json","r") as f:
                status=json.load(f)
                f.close()
            if status == "done":
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    content=f"已经干完活了~ 主人可以新增任务哦~",
                    msg_id=message.id,
                    )
            elif status == "busy":
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    content=f"活还没干完呢~ 主人可以喝杯茶等一下哦~",
                    msg_id=message.id,
                    )
        elif "/help" in message.content:
            await self.api.post_dms(
                    guild_id=message.guild_id,
                    content=f"给主人看看我学会的技能哦~\n输入 /下载学科网 ：跟随指引可以下载高中学段的课件试卷以及教案等资料，并且可以自动发到你的邮箱里去哦~\n未来我还会学习更多技能的，请主人看好我哦~",
                    msg_id=message.id,
                    )
        else:
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"(一脸睿智的表情看着你~)",
                msg_id=message.id,
                )
            
            

    async def on_at_message_create(self, message: Message):
        if "/私信" in message.content:
            dms_payload = await self.api.create_dms(message.guild_id, message.author.id)
            _log.info("发送私信")
            await self.api.post_dms(dms_payload["guild_id"], content="hello", msg_id=message.id)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(direct_message=True, public_guild_messages=True)
    client = SakuraClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])