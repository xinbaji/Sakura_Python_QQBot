import json


appid=input("请输入机器人的appid(按回车键结束): ")
secret=input("请输入机器人的密钥(按回车键结束): ")
config = {
    "appid":appid,
    "secret":secret
}
with open ("config.json","w") as f:
    json.dump(config,f)

print("生成config.json文件成功！")