import json
import random
import statistics
import time

import jwt
from django.conf import settings
from django.http import JsonResponse
# from django.utils.decorators import method_decorator
from django.views import View
# from tools.logging_decorator import logging_check
# from tools.make_token import make_token
from tools.createOrderClient import CreateOrder
from users.models import UserProfile, HistoryOrder, OrderItems, VendorProfile
from items.models import ItemProfile, FavorItem, CartItems, ScoreItem
# from django.shortcuts import render


# Create your views here.
# 商品展示
def item_view(request, item_id):
    if request.method != 'GET':
        result = {'code': 10402, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    token = request.META.get('HTTP_AUTHORIZATION')
    # 有登入
    if token != 'null':
        # 驗證token
        key = settings.JWT_TOKEN_KEY
        try:
            token_check = jwt.decode(token, key, algorithms='HS256')
        except Exception as e:
            print('jwt decode error is %s' % (e))
            result = {'code': 200, 'data': {'favor_list': []}}
        else:
            # 獲取登入用戶
            username = token_check['username']
            user = UserProfile.objects.get(username=username)
            # 查看用戶是否啟用
            if user.active != True:
                result = {'code': 403, 'error': '此用戶不存在！！'}
                return JsonResponse(result)
            favor_list = FavorItem.objects.filter(active=True, username_id=user.username).values_list('itemname_id',
                                                                                                      flat=True)
            result = {'code': 200, 'username': user.username, 'token': True, 'permission': user.permission,
                      'data': {'favor_list': list(favor_list)}}
    else:
        # 沒登入
        result = {'code': 200, 'data': {}}

    item_res = []
    i = {}

    try:
        show_item = ItemProfile.objects.get(id=item_id, active=True)
    except Exception as e:
        result = {'code': 10403, 'error': '此商品已下架'}
        return JsonResponse(result)
    # 取得商品分數list
    item_score = ScoreItem.objects.filter(item_id=item_id, active=True).values_list('item_score',flat=True)
    if len(item_score)==0:
        i['score'] = False
    else:
        avg = statistics.mean(item_score)
        avg_score = format(avg,'.2f')
        i['score'] = avg_score
        i['score_times'] = len(item_score)
    i['item_name'] = show_item.item_name
    i['price'] = format(show_item.price, ',')
    i['pic'] = str(show_item.pic)
    item_res.append(i)
    result['data']['show_item'] = item_res
    result['data']['item_name'] = show_item.item_name

    return JsonResponse(result)


# 搜尋結果
def search_view(request):
    if request.method != 'GET':
        result = {'code': 10401, 'error': '通讯方式错误！！'}
        return JsonResponse(result)
    # 分辨查詢字串
    c = request.GET.get('c')
    kw = request.GET.get('kw')
    if not c and not kw:
        all_item = ItemProfile.objects.filter(active=True)
    if c and kw:
        all_item = ItemProfile.objects.filter(active=True, item_class=c, item_name__icontains=kw)
    else:
        if c:
            all_item = ItemProfile.objects.filter(active=True, item_class=c)
        if kw:
            all_item = ItemProfile.objects.filter(active=True, item_name__icontains=kw)

    token = request.META.get('HTTP_AUTHORIZATION')
    # 有登入
    if token != 'null':
        # 驗證token
        key = settings.JWT_TOKEN_KEY
        try:
            token_check = jwt.decode(token, key, algorithms='HS256')
        except Exception as e:
            print('jwt decode error is %s' % (e))
            result = {'code': 200, 'data': {'favor_list': []}}
        else:
            # 獲取登入用戶
            username = token_check['username']
            user = UserProfile.objects.get(username=username)
            # 查看用戶是否啟用
            if user.active != True:
                result = {'code': 403, 'error': '此用戶不存在！！'}
                return JsonResponse(result)
            favor_list = FavorItem.objects.filter(active=True, username_id=user.username).values_list('itemname_id',
                                                                                                      flat=True)

            result = {'code': 200, 'username': user.username, 'token': True, 'permission': user.permission,
                      'data': {'favor_list': list(favor_list)}}
    else:
        # 沒登入
        result = {'code': 200, 'data': {}}
    item_res = []
    for items in all_item:
        i = {}
        i['id'] = items.id
        i['item_name'] = items.item_name
        i['price'] = format(items.price, ',')
        i['pic'] = str(items.pic)
        item_res.append(i)
    result['data']['all_item'] = item_res

    return JsonResponse(result)


# 跳轉paypal頁面
def check_out(request):
    if request.method != 'POST':
        result = {'code': 10407, 'error': '通讯方式错误！！'}
        return JsonResponse(result)
    # 獲取前端資訊
    json_str = request.body
    json_obj = json.loads(json_str)
    delivery = json_obj['delivery']
    pay_method = json_obj['pay_method']
    # u_name = json_obj['user_name']
    # u_phone = json_obj['user_phone']
    # u_email = json_obj['user_email']
    r_name = json_obj['recipient_name']
    r_phone = json_obj['recipient_phone']
    r_email = json_obj['recipient_email']
    r_addr = json_obj['recipient_addr']
    total_amount = json_obj['total_amount']
    # 創建訂單編號
    today = time.localtime()
    year = today.tm_year  # int
    month = today.tm_mon  # int
    year_mon = str(year) + str(month).zfill(2)  # str
    last_num = HistoryOrder.objects.filter(order_num__icontains=year_mon).order_by('order_num').last()
    num = int(last_num.order_num[6:])
    order_num = year_mon + str(num + 1).zfill(6)
    # 建立paypal訂單資訊
    def paypalCreateResponse(response):
        data = {}
        data["code"] = response.status_code
        data["status"] = response.result.status
        data["orderid"] = response.result.id
        data["intent"] = response.result.intent
        data["links"] = {}
        for link in response.result.links:
            data["links"][link.rel] = link.href
        data["total_Amount"] = response.result.purchase_units[0].amount.value
        return data
    # 判斷有無登入
    token = request.META.get('HTTP_AUTHORIZATION')
    if token != 'null':
        # 驗證token
        key = settings.JWT_TOKEN_KEY
        try:
            token_check = jwt.decode(token, key, algorithms='HS256')
        except Exception as e:
            # 登入失敗
            print('jwt decode error is %s' % (e))
            order = HistoryOrder.objects.create(order_num=order_num, name=r_name, total_amount=total_amount,
                                                addr=r_addr, phone=r_phone, email=r_email)
            # 獲取購物車內容
            json_cart_list = json_obj['cart_list']
            cart_list = json.loads(json_cart_list)
            for item in cart_list:
                item_id = item['item_id']
                cart_item = ItemProfile.objects.get(id=item_id)
                if not cart_item.active:
                    cart_list.remove(item)
                    result = {'code': 10408, 'no_active': cart_item.item_name}
                    return JsonResponse(result)
                OrderItems.objects.create(order_num=order, item_name=cart_item.item_name, item_price=cart_item.price,
                                          item_size=item['item_size'], item_num=item['item_num'])
            result = {'code': 200}
            return JsonResponse(result)

        else:
            # 獲取登入用戶
            username = token_check['username']
            user = UserProfile.objects.get(username=username)
            # 查看用戶是否啟用
            if user.active != True:
                result = {'code': 403, 'error': '此用戶不存在！！'}
                return JsonResponse(result)
            # 登入成功
            result = {'code': 200,'data':{}}
            # 建立paypal付款訂單
            try:
                paypal_response = CreateOrder().create_order('TWD',total_amount)
            except Exception as e:
                result = {'code':10410,'error':e}
                return JsonResponse(result)
            else:
                data = paypalCreateResponse(paypal_response)
                result['data'] = data
                result['pay_url'] = data['links']['approve']
            # 利用顧客帳號下訂單
            order = HistoryOrder.objects.create(order_num=order_num, ordername=user.username, name=r_name,
                                                total_amount=total_amount, addr=r_addr, phone=r_phone, email=r_email)
            # 儲存顧客姓名
            user.name = r_name
            user.save()
            # 獲取購物車內容
            cart_items = CartItems.objects.filter(order_name=user)
            for cart_item in cart_items:
                # 判斷有無商品
                if not cart_item.item_name.active:
                    cart_item.delete()
                    result = {'code':10408,'no_active':cart_item.item_name.item_name}
                    return JsonResponse(result)
                OrderItems.objects.create(order_num=order, item_name=cart_item.item_name.item_name,
                                          item_price=cart_item.item_name.price, item_size=cart_item.item_size,
                                          item_num=cart_item.item_num)
            cart_items.delete()

            return JsonResponse(result)
    # 登入失敗/未註冊/沒登入
    else:
        order = HistoryOrder.objects.create(order_num=order_num, name=r_name, total_amount=total_amount, addr=r_addr,
                                            phone=r_phone, email=r_email)
        # 獲取購物車內容
        json_cart_list = json_obj['cart_list']
        cart_list = json.loads(json_cart_list)
        for item in cart_list:
            item_id = item['item_id']
            cart_item = ItemProfile.objects.get(id=item_id)
            if not cart_item.active:
                cart_list.remove(item)
                result = {'code': 10408, 'no_active': cart_item.item_name}
                return JsonResponse(result)
            OrderItems.objects.create(order_num=order, item_name=cart_item.item_name, item_price=cart_item.price,
                                      item_size=item['item_size'], item_num=item['item_num'])
        result = {'code': 200}
        return JsonResponse(result)

# 確認有無付款
def confirm_paypal(request):
    if request.method != 'POST':
        result = {'code': 10407, 'error': '通讯方式错误！！'}
        return JsonResponse(result)
    # 獲取前端資訊
    json_str = request.body
    json_obj = json.loads(json_str)
    delivery = json_obj['delivery']
    pay_method = json_obj['pay_method']
    # u_name = json_obj['user_name']
    # u_phone = json_obj['user_phone']
    # u_email = json_obj['user_email']
    r_name = json_obj['recipient_name']
    r_phone = json_obj['recipient_phone']
    r_email = json_obj['recipient_email']
    r_addr = json_obj['recipient_addr']
    total_amount = json_obj['total_amount']
    # 創建訂單編號
    today = time.localtime()
    year = today.tm_year  # int
    month = today.tm_mon  # int
    year_mon = str(year) + str(month).zfill(2)  # str
    last_num = HistoryOrder.objects.filter(order_num__icontains=year_mon).order_by('order_num').last()
    num = int(last_num.order_num[6:])
    order_num = year_mon + str(num + 1).zfill(6)
    # 建立paypal訂單資訊
    def paypalCreateResponse(response):
        data = {}
        data["code"] = response.status_code
        data["status"] = response.result.status
        data["orderid"] = response.result.id
        data["intent"] = response.result.intent
        data["links"] = {}
        for link in response.result.links:
            data["links"][link.rel] = link.href
        data["total_Amount"] = response.result.purchase_units[0].amount.value
        return data
    # 判斷有無登入
    token = request.META.get('HTTP_AUTHORIZATION')
    if token != 'null':
        # 驗證token
        key = settings.JWT_TOKEN_KEY
        try:
            token_check = jwt.decode(token, key, algorithms='HS256')
        except Exception as e:
            # 登入失敗
            print('jwt decode error is %s' % (e))
            order = HistoryOrder.objects.create(order_num=order_num, name=r_name, total_amount=total_amount,
                                                addr=r_addr, phone=r_phone, email=r_email)
            # 獲取購物車內容
            json_cart_list = json_obj['cart_list']
            cart_list = json.loads(json_cart_list)
            for item in cart_list:
                item_id = item['item_id']
                cart_item = ItemProfile.objects.get(id=item_id)
                if not cart_item.active:
                    cart_list.remove(item)
                    result = {'code': 10408, 'no_active': cart_item.item_name}
                    return JsonResponse(result)
                OrderItems.objects.create(order_num=order, item_name=cart_item.item_name, item_price=cart_item.price,
                                          item_size=item['item_size'], item_num=item['item_num'])
            result = {'code': 200}
            return JsonResponse(result)

        else:
            # 獲取登入用戶
            username = token_check['username']
            user = UserProfile.objects.get(username=username)
            # 查看用戶是否啟用
            if user.active != True:
                result = {'code': 403, 'error': '此用戶不存在！！'}
                return JsonResponse(result)
            # 登入成功
            result = {'code': 200,'data':{}}
            # 建立paypal付款訂單
            try:
                paypal_response = CreateOrder().create_order('TWD',total_amount)
            except Exception as e:
                result = {'code':10410,'error':e}
                return JsonResponse(result)
            else:
                data = paypalCreateResponse(paypal_response)
                result['data'] = data
            # 利用顧客帳號下訂單
            order = HistoryOrder.objects.create(order_num=order_num, ordername=user.username, name=r_name,
                                                total_amount=total_amount, addr=r_addr, phone=r_phone, email=r_email)
            # 儲存顧客姓名
            user.name = r_name
            user.save()
            # 獲取購物車內容
            cart_items = CartItems.objects.filter(order_name=user)
            for cart_item in cart_items:
                # 判斷有無商品
                if not cart_item.item_name.active:
                    cart_item.delete()
                    result = {'code':10408,'no_active':cart_item.item_name.item_name}
                    return JsonResponse(result)
                OrderItems.objects.create(order_num=order, item_name=cart_item.item_name.item_name,
                                          item_price=cart_item.item_name.price, item_size=cart_item.item_size,
                                          item_num=cart_item.item_num)
            cart_items.delete()

            return JsonResponse(result)
    # 登入失敗/未註冊/沒登入
    else:
        order = HistoryOrder.objects.create(order_num=order_num, name=r_name, total_amount=total_amount, addr=r_addr,
                                            phone=r_phone, email=r_email)
        # 獲取購物車內容
        json_cart_list = json_obj['cart_list']
        cart_list = json.loads(json_cart_list)
        for item in cart_list:
            item_id = item['item_id']
            cart_item = ItemProfile.objects.get(id=item_id)
            if not cart_item.active:
                cart_list.remove(item)
                result = {'code': 10408, 'no_active': cart_item.item_name}
                return JsonResponse(result)
            OrderItems.objects.create(order_num=order, item_name=cart_item.item_name, item_price=cart_item.price,
                                      item_size=item['item_size'], item_num=item['item_num'])
        result = {'code': 200}
        return JsonResponse(result)

class ItemViews(View):
    # 首頁
    def get(self, request):
        c = request.GET.get('c')
        print(c)
        token = request.META.get('HTTP_AUTHORIZATION')
        # 有登入
        if token != 'null':
            # 驗證token
            key = settings.JWT_TOKEN_KEY
            try:
                token_check = jwt.decode(token, key, algorithms='HS256')
            except Exception as e:
                print('jwt decode error is %s' % (e))
                result = {'code': 200, 'data': {'favor_list': []}}
            else:
                # 獲取登入用戶
                username = token_check['username']
                user = UserProfile.objects.get(username=username)
                # 查看用戶是否啟用
                if user.active != True:
                    result = {'code': 403, 'error': '此用戶不存在！！'}
                    return JsonResponse(result)
                favor_list = FavorItem.objects.filter(active=True, username_id=user.username).values_list('itemname_id',
                                                                                                          flat=True)

                result = {'code': 200, 'username': user.username, 'token': True, 'permission': user.permission,
                          'data': {'favor_list': list(favor_list)}}
        else:
            # 沒登入
            result = {'code': 200, 'data': {}}
        if c:
            rd_list_id = ItemProfile.objects.filter(active=True, item_class=c).values_list('id', flat=True)
        else:
            # objects.order_by('?')----->隨機排序
            show_items_list_id = ItemProfile.objects.filter(active=True).values_list('id', flat=True)
            if len(show_items_list_id) < 9:
                K = len(show_items_list_id)
            else:
                K = 9
            rd_list_id = random.sample(list(show_items_list_id), k=K)  # [1,2,3,4,5,6,7,8,9] k=抓取幾個

        item_res = []
        for rd_id in rd_list_id:
            show_item = ItemProfile.objects.get(id=rd_id)
            i = {}
            i['id'] = show_item.id
            i['item_name'] = show_item.item_name
            i['item_price'] = format(show_item.price, ',')
            i['item_pic'] = str(show_item.pic)
            item_res.append(i)

        result['data']['show_items'] = item_res
        return JsonResponse(result)

    # 查看購物車
    def post(self, request):
        # 從前端獲取數據
        json_str = request.body
        json_obj = json.loads(json_str)
        json_cart_list = json_obj['cart_list']
        # 判斷瀏覽器有無現存購物車清單
        if not json_cart_list:
            cart_list = []
        else:
            cart_list = json.loads(json_cart_list)

        # 有登入
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != 'null':
            # 驗證token
            key = settings.JWT_TOKEN_KEY
            try:
                token_check = jwt.decode(token, key, algorithms='HS256')
            except Exception as e:
                # 登入不成功--->取瀏覽器資料
                print('jwt decode error is %s' % (e))
                result = {'code': 200, 'data': {}}
                # print(cart_list)
                # [{'item_id': '10', 'item_size': 'S', 'item_num': '1'},
                #  {'item_id': '10', 'item_size': 'M', 'item_num': '1'},
                #  {'item_id': '10', 'item_size': 'L', 'item_num': '1'}]
                cartlist = []
                for item in cart_list:
                    item_id = item['item_id']
                    cart_item = ItemProfile.objects.get(id=item_id)
                    c = {}
                    # 判斷有無商品
                    if not cart_item.active:
                        cart_list.remove(item)
                        result = {'code': 10408, 'no_active': cart_item.item_name}
                        return JsonResponse(result)
                    c['item_id'] = item_id
                    c['item_pic'] = str(cart_item.pic)
                    c['item_name'] = cart_item.item_name
                    c['item_price'] = format(cart_item.price, ',')
                    c['item_size'] = item['item_size']
                    c['item_num'] = item['item_num']
                    cartlist.append(c)
                result['data']['my_cart'] = cartlist
                return JsonResponse(result)
            else:
                # 獲取登入用戶
                username = token_check['username']
                user = UserProfile.objects.get(username=username)
                # 查看用戶是否啟用
                if user.active != True:
                    result = {'code': 403, 'error': '此用戶不存在！！'}
                    return JsonResponse(result)
                # 成功登入後加入未登入前的購物車內容
                for item in cart_list:
                    item_id = item['item_id']
                    item_size = item['item_size']
                    item_num = item['item_num']
                    try:
                        cart_item = CartItems.objects.get(order_name=user, item_name_id=item_id, item_size=item_size)
                    except Exception as e:
                        CartItems.objects.create(order_name=user, item_name_id=item_id, item_size=item_size,
                                                 item_num=item_num)
                    else:
                        cart_item.item_num = cart_item.item_num + int(item_num)
                        cart_item.save()
                # 成功登入後取數據庫資料
                cart_items = CartItems.objects.filter(order_name=user)
                result = {'code': 200, 'token': True, 'name': user.name, 'phone': user.phone, 'email': user.email, 'addr': user.addr, 'data': {}}
                cartlist = []
                for cart_item in cart_items:
                    c = {}
                    # 判斷有無商品
                    if not cart_item.item_name.active:
                        cart_item.delete()
                        result = {'code': 10408, 'no_active': cart_item.item_name.item_name}
                        return JsonResponse(result)
                    c['cart_id'] = cart_item.id
                    c['item_id'] = cart_item.item_name.id
                    c['item_pic'] = str(cart_item.item_name.pic)
                    c['item_name'] = cart_item.item_name.item_name
                    c['item_price'] = format(cart_item.item_name.price, ',')
                    c['item_size'] = cart_item.item_size
                    c['item_num'] = cart_item.item_num
                    cartlist.append(c)
                result['data']['my_cart'] = cartlist
                return JsonResponse(result)
        # 沒登入存瀏覽器
        else:
            result = {'code': 200, 'data': {}}
            # print(cart_list)
            # [{'item_id': '10', 'item_size': 'S', 'item_num': '1'},
            #  {'item_id': '10', 'item_size': 'M', 'item_num': '1'},
            #  {'item_id': '10', 'item_size': 'L', 'item_num': '1'}]
            cartlist = []
            for item in cart_list:
                item_id = item['item_id']
                cart_item = ItemProfile.objects.get(id=item_id)
                c = {}
                # 判斷有無商品
                if not cart_item.active:
                    cart_list.remove(item)
                    result = {'code': 10408, 'no_active': cart_item.item_name}
                    return JsonResponse(result)

                c['item_id'] = item_id
                c['item_pic'] = str(cart_item.pic)
                c['item_name'] = cart_item.item_name
                c['item_price'] = format(cart_item.price, ',')
                c['item_size'] = item['item_size']
                c['item_num'] = item['item_num']
                cartlist.append(c)
            result['data']['my_cart'] = cartlist
            return JsonResponse(result)


class CartViews(View):
    # 暫無功能
    def get(self, request):
        pass

    # 加入購物車
    def post(self, request):
        # 從前端獲取數據
        json_str = request.body
        json_obj = json.loads(json_str)
        item_id = json_obj['item_id']
        item_size = json_obj['item_size']
        item_num = json_obj['item_num']
        json_cart_list = json_obj['cart_list']
        # 商品數量不能小於1
        if int(item_num) < 1:
            result = {'code': 10409, 'error': '商品數量不能小於1件！！'}
            return JsonResponse(result)
        # 商品數量不能超過10
        if int(item_num) > 10:
            result = {'code': 10404, 'error': '商品數量不能超過10件，如須大量購買請洽尋我們！！'}
            return JsonResponse(result)
        # 判斷瀏覽器有無現存購物車清單
        if not json_cart_list:
            cart_list = []
        else:
            cart_list = json.loads(json_cart_list)
        # 有登入存數據庫
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != 'null':
            # 驗證token
            key = settings.JWT_TOKEN_KEY
            try:
                token_check = jwt.decode(token, key, algorithms='HS256')
            except Exception as e:
                # 登入不成功--->存瀏覽器
                print('jwt decode error is %s' % (e))
                result = {'code': 201, 'data': {}}
                if cart_list:
                    for item in cart_list:
                        if item['item_id'] == item_id and item['item_size'] == item_size:
                            sameitem = True
                            break
                        if item['item_id'] != item_id or item['item_size'] != item_size:
                            sameitem = False
                    if sameitem:
                        item['item_num'] = str(int(item_num) + int(item['item_num']))
                    else:
                        c = {}
                        c['item_id'] = item_id
                        c['item_size'] = item_size
                        c['item_num'] = item_num
                        cart_list.append(c)
                else:
                    c = {}
                    c['item_id'] = item_id
                    c['item_size'] = item_size
                    c['item_num'] = item_num
                    cart_list.append(c)
                result['data']['cart_list'] = cart_list
                return JsonResponse(result)
            else:
                # 獲取登入用戶
                username = token_check['username']
                user = UserProfile.objects.get(username=username)
                # 查看用戶是否啟用
                if user.active != True:
                    result = {'code': 403, 'error': '此用戶不存在！！'}
                    return JsonResponse(result)

                # 成功登入後新增數據庫
                # 判斷數據庫中是否已有相同尺寸的此商品
                try:
                    cart_item = CartItems.objects.get(order_name=user, item_name_id=item_id, item_size=item_size)
                except Exception as e:
                    CartItems.objects.create(order_name=user, item_name_id=item_id, item_size=item_size,
                                             item_num=item_num)
                else:
                    cart_item.item_num = cart_item.item_num + int(item_num)
                    cart_item.save()
                result = {'code': 200}
                return JsonResponse(result)
        # 沒登入存瀏覽器
        else:
            result = {'code': 201, 'data': {}}
            if cart_list:
                for item in cart_list:
                    if item['item_id'] == item_id and item['item_size'] == item_size:
                        sameitem = True
                        break
                    if item['item_id'] != item_id or item['item_size'] != item_size:
                        sameitem = False
                if sameitem:
                    item['item_num'] = str(int(item_num) + int(item['item_num']))
                else:
                    c = {}
                    c['item_id'] = item_id
                    c['item_size'] = item_size
                    c['item_num'] = item_num
                    cart_list.append(c)

            else:
                c = {}
                c['item_id'] = item_id
                c['item_size'] = item_size
                c['item_num'] = item_num
                cart_list.append(c)
            result['data']['cart_list'] = cart_list
            return JsonResponse(result)

    # 從購物車刪除
    def delete(self, request):
        # 從前端獲取數據
        json_str = request.body
        json_obj = json.loads(json_str)
        cart_id = json_obj['cart_id']
        # 有登入
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != 'null':
            # 驗證token
            key = settings.JWT_TOKEN_KEY
            try:
                token_check = jwt.decode(token, key, algorithms='HS256')
            except Exception as e:
                # 登入不成功--->刪瀏覽器資料
                print('jwt decode error is %s' % (e))
                json_cart_list = json_obj['cart_list']
                cart_list = json.loads(json_cart_list)
                del cart_list[int(cart_id)]
                result = {'code': 201, 'data': {}}
                result['data']['cart_list'] = cart_list
                return JsonResponse(result)
            else:
                # 獲取登入用戶
                username = token_check['username']
                user = UserProfile.objects.get(username=username)
                # 查看用戶是否啟用
                if user.active != True:
                    result = {'code': 403, 'error': '此用戶不存在！！'}
                    return JsonResponse(result)
                # 成功登入後刪除數據庫資料
                del_cart = CartItems.objects.get(id=cart_id)
                del_cart.delete()
                result = {'code': 200}
                return JsonResponse(result)
        # 沒登入刪瀏覽器資料
        else:
            json_cart_list = json_obj['cart_list']
            cart_list = json.loads(json_cart_list)
            del cart_list[int(cart_id)]
            result = {'code': 201, 'data': {}}
            result['data']['cart_list'] = cart_list
            return JsonResponse(result)

    # 更新購物車
    def put(self, request):
        # 從前端獲取數據
        json_str = request.body
        json_obj = json.loads(json_str)
        new_list = json_obj['new_list']
        # 數量不可為空或符號
        i = 0
        while i < len(new_list):
            item_num = new_list[i][1]
            try:
                int(item_num)
            except Exception as e:
                result = {'code': 10406, 'error': '商品資訊輸入錯誤！！'}
                return JsonResponse(result)
            i += 1
        # 商品數量不能超過10
        i = 0
        while i < len(new_list):
            item_num = new_list[i][1]
            if int(item_num) > 10:
                result = {'code': 10405, 'error': '商品數量不能超過10件，如須大量購買請洽尋我們！！'}
                return JsonResponse(result)
            i += 1
        # 有登入改數據庫
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != 'null':

            # 驗證token
            key = settings.JWT_TOKEN_KEY
            try:
                token_check = jwt.decode(token, key, algorithms='HS256')
            except Exception as e:
                # 登入不成功--->修改瀏覽器
                print('jwt decode error is %s' % (e))
                json_cart_list = json_obj['cart_list']
                cart_list = json.loads(json_cart_list)
                i = 0
                while i < len(new_list):
                    if int(new_list[i][1]) == 0:
                        del cart_list[int(new_list[i][0])]
                    else:
                        cart_list[int(new_list[i][0])]['item_num'] = int(new_list[i][1])
                    i += 1
                result = {'code': 201, 'data': {}}
                result['data']['cart_list'] = cart_list
                return JsonResponse(result)
            else:
                # 獲取登入用戶
                username = token_check['username']
                user = UserProfile.objects.get(username=username)
                # 查看用戶是否啟用
                if user.active != True:
                    result = {'code': 403, 'error': '此用戶不存在！！'}
                    return JsonResponse(result)
                # 成功登入後修改數據庫
                a = 0
                while a < len(new_list):
                    cart_id = new_list[a][0]
                    if int(new_list[a][1]) == 0:
                        new_cart = CartItems.objects.get(id=cart_id)
                        new_cart.delete()
                    else:
                        new_cart = CartItems.objects.get(id=cart_id)
                        new_cart.item_num = int(new_list[a][1])
                        new_cart.save()
                    a += 1
                result = {'code': 200}
                return JsonResponse(result)
        # 沒登入改瀏覽器
        else:
            json_cart_list = json_obj['cart_list']
            cart_list = json.loads(json_cart_list)
            # print(cart_list)
            # [{'item_id': '38', 'item_size': 'S', 'item_num': '1'}, {'item_id': '8', 'item_size': 'S', 'item_num': '1'}]
            # print(new_list)
            # [['0', '2'], ['1', '2']]
            i = 0
            while i < len(new_list):
                if int(new_list[i][1]) == 0:
                    del cart_list[int(new_list[i][0])]
                else:
                    cart_list[int(new_list[i][0])]['item_num'] = int(new_list[i][1])
                i += 1
            result = {'code': 201, 'data': {}}
            result['data']['cart_list'] = cart_list
            return JsonResponse(result)
