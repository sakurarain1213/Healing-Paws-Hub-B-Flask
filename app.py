import json
# import time

from flask import Flask, jsonify, request, redirect, url_for, Response, stream_with_context


import GPTserver

app = Flask(__name__)  # 实例化


@app.route('/')
def hello_world():  # 定义路由，请求地址为/的时候，路由跳转到hello_flask()这个函数   route可以有多个 同时可用
    return 'Hello World!'


@app.route('/abab')
def abab():  # 定义路由，请求地址为/的时候，路由跳转到hello_flask()这个函数
    data = {
        "name": "ko",
        "age": 18,
        "sex": "female"
    }
    return jsonify(data)


@app.route('/hello/<name>')  # url传参
def hello_name(name):
    return 'Hello %s!' % name


@app.route('/login', methods=['POST', 'GET'])  # 默认GET 但是可以设置
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


@app.route('/create_conversation', methods=['POST'])
def create_conversation_endpoint():
    conversation_id = GPTserver.create_conversation()
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {'conversation_id': conversation_id}
    }), 200


@app.route('/blocking_conversation', methods=['POST'])
def blocking_conversation_endpoint():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    msg = data.get('msg')
    if not conversation_id or not msg:
        return jsonify({
            'code': -100,
            'msg': 'error',
            'data': {'error': 'Missing conversation_id or msg'}
        }), 400
    response = GPTserver.blocking_conversation(conversation_id, msg)
    return jsonify({'success': True, 'data': response}), 200


# @app.route('/streaming_conversation', methods=['POST'])
# def streaming_conversation_endpoint():
#     # 首先获取请求数据
#     data = request.get_json()
#     conversation_id = data.get('conversation_id')
#     msg = data.get('msg')
#     # 检查数据是否完整
#     if not conversation_id or not msg:
#         return jsonify({'error': 'Missing conversation_id or msg'}), 400
#         # 定义生成器函数，不再依赖于请求上下文 才不会报错
#
#     def stream_response():
#         for text in GPTserver.streaming_conversation(conversation_id, msg):
#             yield json.dumps({'text': text}).encode('utf-8')
#             # 返回响应流
#
#     return Response(stream_response(), mimetype='application/json')


@app.route('/streaming_conversation', methods=['POST'])
def streaming_conversation_endpoint():
    # 首先获取请求数据
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    msg = data.get('msg')
    # 检查数据是否完整
    if not conversation_id or not msg:
        return jsonify({
            'code': -100,
            'msg': 'error',
            'data': {'error': 'Missing conversation_id or msg'}
        }), 400
        # 定义生成器函数，不再依赖于请求上下文 才不会报错

    def stream_response():
        for text in GPTserver.streaming_conversation(conversation_id, msg):
            yield json.dumps({'event': "message",
                              'id': conversation_id,
                             'data': text}).encode('utf-8')

    # 返回响应流
    return Response(stream_with_context(stream_response()), mimetype='text/event-stream')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # 这是默认值 可以自己改  0.0.0.0代表全部可访问  127.0.0.1只能本地访问   debug在发布的时候要false

# 打包前生成requirements.txt  命令是pip freeze > requirements.txt
# 随后直接将文件夹拷贝到服务器硬盘即可
# 注意面板里要设置python项目启动 而不是uwsgi服务器
# 更新项目只需要重传py文件和面板项目重启即可


# 考虑实现对话存储到数据库  和 地址的token鉴权
