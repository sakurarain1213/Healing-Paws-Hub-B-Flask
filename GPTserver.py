# pip install --upgrade appbuilder-sdk -i https://pypi.tuna.tsinghua.edu.cn/simple  控制台虚拟环境运行 国内镜像下载快

import appbuilder
import os

# 注意以下示例正确运行依赖的条件包括：
# 1. 在百度智能云千帆AppBuilder官网使用AgentBuilder创建应用且应用已发布
# 2. 密钥正确有效
# 3. 密钥需要与发布应用正确对应，即需要使用发布应用的账户下的密钥
# GPT的调用见 https://github.com/baidubce/app-builder/blob/master/cookbooks/agent_builder.ipynb
# 配置密钥与应用ID
# 应用的自定义知识在百度千帆平台修改即可  对应改app_id
# 建议服务器的python版本在3.10.0及以上！！！ 不然会出现依赖错误
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-lp91La4lRwuifo4dSNURU/70cb3ab0e2e87e267f6840f76e9fd052adfca877"
app_id = "20f7b7b9-0c09-4e28-8f6c-5fe01ca115c1"

'''
# 初始化Agent
agent_builder = appbuilder.AgentBuilder(app_id)

# 创建会话ID
conversation_id = agent_builder.create_conversation()

print("对话id是：", conversation_id)
# 阻塞式对话
msg = agent_builder.run(conversation_id, "你好 你是谁")
print("ans：", msg.content.answer)

# 流式对话
msg = agent_builder.run(conversation_id, "上一句话是什么", stream=True)
for content in msg.content:
    for ev in content.events:
        # ev内容是code=0 message='' status='running'event_type='ChatAgent' content_type='text' detail={'text': '上一句话'}
        # status有preparing running  done success这几种
        # print(ev)
        if ev.status == 'running':
            text_value = ev.detail['text']
            print(text_value)
'''


def create_conversation():  # 会返回新对话的id  初始化
    agent_builder = appbuilder.AgentBuilder(app_id)
    return agent_builder.create_conversation()


def blocking_conversation(conversation_id, msg):  # 阻塞对话函数
    agent_builder = appbuilder.AgentBuilder(app_id)
    response = agent_builder.run(conversation_id, msg)
    return response.content.answer


def streaming_conversation(conversation_id, msg):  # 流式对话函数
    agent_builder = appbuilder.AgentBuilder(app_id)
    response = agent_builder.run(conversation_id, msg, stream=True)
    for content in response.content:
        for ev in content.events:
            if ev.status == 'running':
                # print(ev.detail['text'])
                yield ev.detail['text']
            elif ev.status == 'done' and ev.event_type == 'ChatAgent':
                yield 'FIN'
