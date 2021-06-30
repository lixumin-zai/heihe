from flask import Flask, request, Response, render_template, make_response, jsonify
from markupsafe import escape
import json
import os
from script import ocr_api, correct_api
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
# # ---------------------使得jsonify返回值中文--------------------------------
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello_world():
    text = "我是旭民"
    res = jsonify({
        'text': text
    })
    return res


# ---------------------------------------------------------------
@app.route('/photo', methods=['POST'])
def get_photo():
    try:
        # -----------------参数待定-----------------------
        # 接收参数username
        username = request.values.get('username')
        # 接收参数page
        page = request.values.get('page')
        # print(username)
        # print(page)
        # request.
        # -----------------------------------------------------
        # 接收图片文件
        upload_file = request.files['file']
        # print(type(upload_file.stream.read()))  ##<class 'bytes'>
        # 获取图片名
        file_name = upload_file.filename.encode('utf-8').decode('unicode_escape')
        # 文件保存目录（桌面）
        # file_path = r'C:/Users/Administrator/Desktop/flask/'
        if upload_file:
            # -----------------------测试部分-----------------------
            # 地址拼接
            # file_paths = os.path.join(file_path, file_name)
            # 保存接收的图片到桌面
            # upload_file.save(file_paths)
            # 随便打开一张其他图片作为结果返回，
            # -----------------------------------------------------
            # ----------------------- 调用模型-----------------------
            bytes_img = upload_file.stream.read()
            text, title, section = ocr_api.call_api(bytes_img)
            text.encode('utf-8').decode('unicode_escape')
            correct, err_num = correct_api.call_api(text)

            # -----------------------------------------------------
            # ----------------------返回参数-----------------------
            res = jsonify({
                'file_name': file_name,
                'username': username,
                'page': page,
                'text': text,
                'correct': correct,
                'title': title,
                'section': section,
                'err_num': err_num
            })
            return res
    except:
        return jsonify({
            'error': "图片识别出错，请调整图片大小参数",
        })



##############################################################################
# def processing_img(img):
#     text = Ocr(img)
#     score, correct, comment = Score(text)


##############################################################################


if __name__ == '__main__':
    # -----------------------------------------------------
    # 加载模型

    # -----------------------------------------------------
    # 启动服务
    # app.config['JSON_AS_ASCII'] = False
    app.run(port=5000, host="0.0.0.0")

# ##############################################################################
# # 您可以通过用 标记部分来向 URL 添加可变部分 <variable_name>。然后您的函数将接收<variable_name> 作为关键字参数。
# # 或者，您可以使用转换器来指定参数的类型，例如<converter:variable_name>.
#
#
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return f'User {escape(username)}'
#
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'
#
#
# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'
#
#
# ##############################################################################
#
#
# from flask import url_for
#
#
# @app.route('/')
# def index():
#     return 'index'
#
#
# @app.route('/login')
# def login():
#     return 'login'
#
#
# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'
#
#
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
#
# ##############################################################################
#
# from flask import request
#
#
# @app.route('/login2', methods=['GET', 'POST'])
# def login2():
#     if request.method == 'POST':
#         return "do_the_login()"
#     else:
#         return "show_the_login_form()"
#
#
# ##############################################################################
#
# @app.route('/123', methods=['GET'])
# def get_text_input():
#     text = request.args.get('inputstr')
#     print(text)
#     return text
#
