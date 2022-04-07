import json
import hashlib

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from tools.logging_decorator import logging_check
from tools.make_token import make_token
from users.models import UserProfile, HistoryOrder, OrderItems, VendorProfile
from items.models import ItemProfile, FavorItem, ScoreItem
from django.shortcuts import render


# Create your views here.

# 更改地址
@logging_check
def user_views(request, username):
    if request.method != 'PUT':
        result = {'code': 10108, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    new_addr = json_obj['new_addr']
    user = request.logging_user

    if not new_addr:
        result = {'code': 10113, 'error': '地址不能為空'}
        return JsonResponse(result)
    user.addr = new_addr
    user.save()
    result = {'code': 200}
    return JsonResponse(result)


# 收藏商品
@logging_check
def add_favor(request, username):
    if request.method != 'PUT':
        result = {'code': 10120, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    user = request.logging_user
    json_str = request.body
    json_obj = json.loads(json_str)
    item_id = json_obj['item_id']

    try:
        favor = FavorItem.objects.get(username_id=user.username, itemname_id=item_id)
    except Exception as e:
        FavorItem.objects.create(username_id=user.username, itemname_id=item_id)
        return JsonResponse({'code': 200})
    else:
        favor.active = True
        favor.save()
    return JsonResponse({'code': 200})


# 取消收藏商品
@logging_check
def del_favor(request, username):
    if request.method != 'PUT':
        result = {'code': 10109, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    user = request.logging_user
    json_str = request.body
    json_obj = json.loads(json_str)
    favor_list_id = json_obj['id']
    item_id = json_obj['item_id']

    if favor_list_id:
        try:
            item = FavorItem.objects.get(id=favor_list_id)
        except Exception as e:
            result = {'code': 10110, 'error': e}
            return JsonResponse(result)
    if item_id:
        try:
            item = FavorItem.objects.get(itemname_id=item_id, username_id=user.username)
        except Exception as e:
            result = {'code': 10121, 'error': e}
            return JsonResponse(result)

    # 取消啟用收藏商品
    item.active = False
    item.save()
    return JsonResponse({'code': 200})


# 商品評分
@logging_check
def score_item(request, username):
    if request.method != 'POST':
        result = {'code': 10122, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    user = request.logging_user
    json_str = request.body
    json_obj = json.loads(json_str)
    item_id = json_obj['item_id']
    score = json_obj['score']

    item = ItemProfile.objects.get(id=item_id)
    ScoreItem.objects.create(username=user, item=item, item_score=score)
    result = {'code': 200}
    return JsonResponse(result)


class UserViews(View):

    @method_decorator(logging_check)
    # /usercenter ----->查看顧客中心
    def get(self, request):

        user = request.logging_user
        # 獲取數據庫資料
        my_order = HistoryOrder.objects.filter(ordername=user.username)
        # my_favor = ItemProfile.objects.filter(favor__username=user.username,active=True)
        favor_time = FavorItem.objects.filter(username_id=user.username, active=True)

        # 數據庫資料轉字典格式
        result = {'code': 200, 'username': user.username, 'data': {'addr': user.addr}}
        order_res = []
        for orders in my_order:
            o = {}
            o['order_num'] = orders.order_num
            o['total_amount'] = format(orders.total_amount, ',')
            o["order_item"] = []
            o['create_time'] = orders.create_time.strftime("%Y-%m-%d")
            # 獲取訂單品項---儲存在訂單下層
            order_items = OrderItems.objects.filter(order_num_id=orders.order_num)
            for ot in order_items:
                t = {}
                t['item_name'] = ot.item_name
                t['item_size'] = ot.item_size
                t['item_price'] = format(ot.item_price, ',')
                t['item_num'] = ot.item_num
                o["order_item"].append(t)
            order_res.append(o)
        result['data']['my_order'] = order_res

        favor_res = []
        for ft in favor_time:
            f = {}
            f['item_id'] = ft.itemname.id
            f['item_name'] = ft.itemname.item_name
            f['price'] = format(ft.itemname.price, ',')
            f['pic'] = str(ft.itemname.pic)
            f['upload_time'] = ft.upload_time.strftime("%Y-%m-%d")
            f['id'] = ft.id
            # 查看有無評分
            try:
                item_score = ScoreItem.objects.get(username=user, item_id=ft.itemname.id, active=True)
            except:
                f['score'] = False
            else:
                f['score'] = item_score.item_score
            favor_res.append(f)
        result['data']['my_favor'] = favor_res
        return JsonResponse(result)

    # /register ----->註冊
    def post(self, request):

        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        pwd_1 = json_obj['pwd_1']
        pwd_2 = json_obj['pwd_2']
        email = json_obj['email']
        phone = json_obj['phone']

        # 檢查參數
        #####帳號是否重複#####
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10101, 'error': '帳號已存在'}
            return JsonResponse(result)
        #####密碼是否小於8個字#####
        if len(pwd_1) < 8:
            result = {'code': 10102, 'error': '密碼少於8個字元'}
            return JsonResponse(result)
        #####密碼是否一致#####
        if pwd_1 != pwd_2:
            result = {'code': 10103, 'error': '兩次密碼不一致，請確認後在輸入'}
            return JsonResponse(result)
        #####表單提交不為空#####
        for a in json_obj.values():
            if not a:
                result = {'code': 10114, 'error': '表單不能為空'}
                return JsonResponse(result)
        # 密碼哈希處理
        m = hashlib.md5()
        m.update(pwd_1.encode())  # 要求是字節串格式
        # 插入UserProfile數據表
        UserProfile.objects.create(username=username, userpwd=m.hexdigest(), email=email, phone=phone)

        # 紀錄登錄狀態
        token = make_token(username)
        result = {'code': 200, 'username': username, 'data': {'token': token}}
        return JsonResponse(result)

    @method_decorator(logging_check)
    # /usercenter ----->更改密碼
    def put(self, request, username):

        json_str = request.body
        json_obj = json.loads(json_str)
        old_pwd = json_obj['old_pwd']
        new_pwd1 = json_obj['new_pwd1']
        new_pwd2 = json_obj['new_pwd2']
        user = request.logging_user

        # 驗證舊密碼
        m = hashlib.md5()
        m.update(old_pwd.encode())
        if user.userpwd != m.hexdigest():
            result = {'code': 10104, 'error': '舊密碼輸入錯誤'}
            return JsonResponse(result)
        # 密碼是否小於8個字
        if len(new_pwd1) < 8:
            result = {'code': 10105, 'error': '密碼少於8個字元'}
            return JsonResponse(result)
        # 密碼是否一致
        if new_pwd1 != new_pwd2:
            result = {'code': 10106, 'error': '兩次密碼不一致，請確認後再輸入'}
            return JsonResponse(result)
        # 新舊密碼是否相同
        if old_pwd == new_pwd1:
            result = {'code': 10107, 'error': '新舊密碼一致，請確認後再輸入'}
            return JsonResponse(result)
        # 密碼哈希處理
        n = hashlib.md5()
        n.update(new_pwd1.encode())  # 要求是字節串格式
        # 更新UserProfile數據表
        user.userpwd = n.hexdigest()
        user.save()
        return JsonResponse({'code': 200})


class VendorViews(View):
    # 廠商註冊
    @method_decorator(logging_check)
    def post(self, request):

        user = request.logging_user
        json_str = request.body
        json_obj = json.loads(json_str)
        company = json_obj['company']
        company_num = json_obj['company_num']
        contact_name = json_obj['contact_name']
        contact_tel = json_obj['contact_tel']
        tel_ext = json_obj['tel_ext']  # 可以為空

        # 表單不能為空
        # print(list(json_obj.values())[:4])
        for a in list(json_obj.values())[:4]:
            if not a:
                result = {'code': 10112, 'error': '表單不能為空'}
                return JsonResponse(result)
        # 插入VendorProfile數據表
        if tel_ext:
            contact_tel = contact_tel + tel_ext
        VendorProfile.objects.create(contactor_id=user.username, company=company, company_num=company_num,
                                     contact_name=contact_name, contact_tel=contact_tel)

        # 修改用戶權限為vendor
        user.permission = 'vendor'
        user.save()

        result = {'code': 200, 'username': user.username, 'data': {}}
        return JsonResponse(result)

    # 廠商頁面
    @method_decorator(logging_check)
    def get(self, request):
        user = request.logging_user
        # 檢查權限
        user_prm = user.permission
        if user_prm != 'vendor':
            result = {'code': 10111, 'error': '您非合作廠商，即將為您跳轉廠商登錄頁面'}
            return JsonResponse(result)
        # 獲取數據庫資料
        all_products = ItemProfile.objects.filter(active=True, vendor__contactor=user.username)

        # 數據庫資料轉字典格式
        result = {'code': 200, 'username': user.username, 'data': {}}
        product_res = []
        for products in all_products:
            i = {}
            i['id'] = products.id
            i['item_name'] = products.item_name
            i['item_num'] = products.item_num
            i['price'] = format(products.price, ',')
            i['pic'] = str(products.pic)
            i['item_class'] = products.item_class
            i['item_amount'] = products.item_amount
            product_res.append(i)
        result['data']['all_products'] = product_res
        return JsonResponse(result)

    # 廠商刪除商品
    @method_decorator(logging_check)
    def delete(self, request):
        if request.method != 'DELETE':
            result = {'code': 10115, 'error': '通讯方式错误！！'}
            return JsonResponse(result)

        json_str = request.body
        json_obj = json.loads(json_str)
        item_id = json_obj['id']

        try:
            item = ItemProfile.objects.get(id=item_id)
        except Exception as e:
            result = {'code': 10116, 'error': e}
            return JsonResponse(result)
        # 取消啟用商品
        item.active = False
        item.save()
        return JsonResponse({'code': 200})

    # 廠商修改商品
    @method_decorator(logging_check)
    def put(self, request):
        # 獲取前端數據
        json_str = request.body
        json_obj = json.loads(json_str)
        item_id = json_obj['id']
        item_num = json_obj['item_num']
        item_name = json_obj['item_name']
        item_price = json_obj['item_price']
        item_amount = json_obj['item_amount']
        item_class = json_obj['item_class']

        # 檢查price,amount是否為數字
        try:
            int(item_price) and int(item_amount)
        except Exception as e:
            result = {'code': 10117, 'error': '商品資訊輸入錯誤！！'}
            return JsonResponse(result)
        # 檢查表單是否為空
        for a in json_obj.values():
            if not a:
                result = {'code': 10118, 'error': '表單不能為空'}
                return JsonResponse(result)
        # 修改商品數據庫
        try:
            edit_item = ItemProfile.objects.get(id=item_id)
        except Exception as e:
            result = {'code': 10119, 'error': '商品不存在！！'}
            return JsonResponse(result)

        edit_item.item_num = item_num
        edit_item.item_name = item_name
        edit_item.price = item_price
        edit_item.item_amount = item_amount
        edit_item.item_class = item_class
        edit_item.save()

        result = {'code': 200}
        return JsonResponse(result)


# 廠商新增商品圖片
@logging_check
def add_item_pic(request):
    if request.method != 'POST':
        result = {'code': 10308, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    add_pic = request.FILES['add_pic']
    new_pic = ItemProfile.objects.create(pic=add_pic, price=0, vendor_id=1, item_amount=0)

    return JsonResponse({'code': 200, 'new_pic': str(new_pic.pic)})


# 廠商新增商品
@logging_check
def add_item(request):
    user = request.logging_user
    json_str = request.body
    json_obj = json.loads(json_str)
    item_num = json_obj['item_num']
    item_name = json_obj['item_name']
    item_price = json_obj['item_price']
    item_amount = json_obj['item_amount']
    item_class = json_obj['item_class']
    # 檢查price,amount是否為數字
    try:
        int(item_price) and int(item_amount)
    except Exception as e:
        result = {'code': 10313, 'error': '商品資訊輸入錯誤！！'}
        return JsonResponse(result)
    # 檢查表單是否為空
    for a in json_obj.values():
        if not a:
            result = {'code': 10314, 'error': '表單不能為空'}
            return JsonResponse(result)
    # 修改商品數據庫
    add_item = ItemProfile.objects.order_by('id').last()
    if add_item.item_name != "":
        result = {'code': 10316, 'error': '請先上傳圖片！！'}
        return JsonResponse(result)

    add_item.item_num = item_num
    add_item.item_name = item_name
    add_item.price = item_price
    add_item.item_amount = item_amount
    add_item.item_class = item_class
    add_item.vendor_id = user.vendorprofile.id
    add_item.save()

    result = {'code': 200}
    return JsonResponse(result)
