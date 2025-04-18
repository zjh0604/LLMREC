import os
import sqlite3

import qianfan

# 【不推荐】使用应用AK/SK调用流程
os.environ["QIANFAN_AK"] = "5W9dFLCns7XBPFMlaYn65ebp"
os.environ["QIANFAN_SK"] = "1pqLwJPyl7aDczuD2yCmS1uydBqbzvr5"

chat_completion = qianfan.ChatCompletion()


# 输入id查询用户信息
def query_id(user_id):
    # 连接数据库
    conn = sqlite3.connect("user.db")
    print("Opened database successfully")
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT * from user_profile_2 where id = " + user_id)
    for row in cursor:
        print("ID = ", row[0])
        print("学习应用使用 = ", row[1])
        print("通信内容 = ", row[2])
        print("社交媒体活动 = ", row[3])
    return row


# 输入id
user_id = input("请输入用户id：")
profile = query_id(user_id)

# 输入操作日志
user_operation_diary = """{
"system_log":{
"learning_platform":{
"usage_count":100,
"time_period":"30 days"
},
"communication_app":{
"self_attention_count":7,
"time_period":"30 days"
},
"social_media":{
"like_count":115,
"comment_count":125,
"share_count":325,
"time_period":"30 days"
}
}
}
"""

user_profile = (
        "用户的三魂六魄画像：id = "
        + user_id
        + ", 学习应用使用 = "
        + str(profile[1])
        + ", 通信内容 = "
        + str(profile[2])
        + ", 社交媒体活动 = "
        + str(profile[3])
        + "."
)

prompt_diary = "以上是该用户的操作日志，请按以下格式进行总结：“用户xx天内操作了xx次xx”...注意不要生成其他的信息，不需要解释你的回答。"

# 指定特定模型
resp = chat_completion.do(
    model="ERNIE-4.0-Turbo-8K",
    messages=[{"role": "user", "content": user_operation_diary + prompt_diary}],
)

# print(resp["body"])
result_summary = resp["result"]
print("***********第1步***********")
print(result_summary)

with open("txtrag_selected_test.txt", "r", encoding="utf-8") as txtrag:
    # 读取文件
    # rag = "用户画像的得分如下：" + txtrag.read()
    rag = txtrag.read()

prompt_profile = """
请根据用户的操作日志，和旧的用户画像，覆盖用户画像分数。
输出格式为：
id=xx\n 旧的学习应用使用=xx\n 旧的通信内容=xx\n 旧的社交媒体活动=xx\n 
新的学习应用使用分数=xx\n 新的通信内容分数=xx\n 新的社交媒体活动分数=xx\n 
学习应用使用的分数变化=xx\n 通信内容的分数变化=xx\n 社交媒体活动的分数变化=xx\n
用户特点=?
"""

# 指定特定模型
resp = chat_completion.do(
    model="ERNIE-4.0-Turbo-8K",
    messages=[
        {
            "role": "user",
            "content": "用户画像："
                       + user_profile
                       + result_summary
                       + prompt_profile
                       + rag,
        }
    ],
)

result_profile = resp["result"]
print("***********第2步***********")
print(result_profile)

# 生成推荐列表
recommended_projects = [
    "4K超高清智能电视",
    "节能型智能洗衣机",
    "多功能电动剃须刀",
    "有机冷压橄榄油",
    "智能跑步机",
    "环保材料制成的休闲鞋",
    "天然成分护肤套装",
    "教育互动机器人",
    "便携式太阳能帐篷灯",
    "可定制的智能壁挂画",
]

prompt_item_list = "请根据用户的操作和画像，生成一个排好序的推荐列表，推荐列表中应该包含3个产品，每个产品的名称应该是一个字符串，输出格式为：产品1\n 产品2\n 产品3\n ..."

# 指定特定模型
resp = chat_completion.do(
    model="ERNIE-4.0-Turbo-8K",
    messages=[
        {
            "role": "user",
            "content": "用户画像："
                       + result_profile
                       + "待推荐的项目列表："
                       + str(recommended_projects)
                       + prompt_item_list,
        }
    ],
)

result_item_list = resp["result"]
print("***********第3步***********")
print(result_item_list)
