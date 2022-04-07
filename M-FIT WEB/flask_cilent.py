from flask import Flask, send_file
import sys


app = Flask(__name__)

@app.route('/index')
def index():
    #首頁
    return send_file('templates/index.html')

@app.route('/login')
def login():
    #登入
    return send_file('templates/login.html')

@app.route('/register')
def register():
    #註冊
    return send_file('templates/register.html')

@app.route('/usercenter')
def usercenter():
    #顧客中心
    return send_file('templates/usercenter.html')

@app.route('/manager')
def manager():
    #管理後台
    return send_file('templates/manager.html')

@app.route('/vendor_regist')
def vendor_regist():
    #廠商註冊
    return send_file('templates/vendor_regist.html')

@app.route('/vendor')
def vendor():
    #廠商作業
    return send_file('templates/vendor.html')

@app.route('/cart')
def cart():
    #購物車
    return send_file('templates/cart.html')

@app.route('/search')
def search():
    #商品清單(分類、搜尋)
    return send_file('templates/search.html')

@app.route('/item/<item_id>')
def item(item_id):
    #商品展示
    return send_file('templates/item.html')

@app.route('/check_out')
def check_out():
    #結帳
    return send_file('templates/check_out.html')

if __name__ == '__main__':
    app.run(debug=True)