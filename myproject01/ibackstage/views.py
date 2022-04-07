import json

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator

from tools.logging_decorator import logging_check
from users.models import UserProfile, VendorProfile, HistoryOrder, OrderItems
from items.models import ItemProfile
from django.db.models import Avg, Max, Min, Count, Sum


# Create your views here.
# 管理者刪除用戶
@logging_check
def del_user(request):
    if request.method != 'PUT':
        result = {'code': 10302, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    user_name = json_obj['id']

    try:
        user = UserProfile.objects.get(username=user_name)
    except Exception as e:
        result = {'code': 10303, 'error': e}
        return JsonResponse(result)
    # 取消啟用用戶
    user.active = False
    user.save()
    return JsonResponse({'code': 200})

# 管理者刪除廠商
@logging_check
def del_vendor(request):
    if request.method != 'PUT':
        result = {'code': 10304, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    vendor_id = json_obj['id']

    try:
        vendor = VendorProfile.objects.get(id=vendor_id)
    except Exception as e:
        result = {'code': 10305, 'error': e}
        return JsonResponse(result)
    # 取消啟用廠商
    vendor.active = False
    vendor.save()
    return JsonResponse({'code': 200})

# 管理者刪除商品
@logging_check
def del_item(request):
    if request.method != 'PUT':
        result = {'code': 10306, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    item_id = json_obj['id']

    try:
        item = ItemProfile.objects.get(id=item_id)
    except Exception as e:
        result = {'code': 10307, 'error': e}
        return JsonResponse(result)
    # 取消啟用商品
    item.active = False
    item.save()
    return JsonResponse({'code': 200})

# 管理者新增商品圖片
@logging_check
def add_item_pic(request):

    if request.method != 'POST':
        result = {'code': 10308, 'error': '通讯方式错误！！'}
        return JsonResponse(result)

    add_pic = request.FILES['add_pic']
    new_pic = ItemProfile.objects.create(pic=add_pic,price=0,vendor_id=1,item_amount=0)

    return JsonResponse({'code': 200,'new_pic':str(new_pic.pic)})


class ManagerViews(View):

    @method_decorator(logging_check)
    # /manager_backstage ----->查看管理後台
    def get(self, request):

        user = request.logging_user
        # 檢查權限
        user_prm = user.permission
        if user_prm != 'manager':
            result = {'code': 10301, 'error': '您非管理者！'}
            return JsonResponse(result)
        # 獲取數據庫資料
        all_user = UserProfile.objects.filter(active=True)
        all_vendor = VendorProfile.objects.filter(active=True)
        all_order = HistoryOrder.objects.filter()
        all_item = ItemProfile.objects.filter(active=True)
        # 更新消費金額
        for u in all_user:
            u_amount = HistoryOrder.objects.filter(ordername=u.username).aggregate(sum_amount=Sum('total_amount'))
            # print(u_amount)
            if u_amount['sum_amount'] != None:
                u.amount = u_amount['sum_amount']
                u.save()
        # 數據庫資料轉字典格式
        result = {'code': 200, 'username': user.username, 'data': {}}

        users_res = []
        for users in all_user:
            u = {}
            u['username'] = users.username
            u['permission'] = users.permission
            u['email'] = users.email
            u['phone'] = users.phone
            u['addr'] = users.addr
            u['amount'] = format(users.amount,',')
            u['create_time'] = users.create_time.strftime("%Y-%m-%d")
            users_res.append(u)
        result['data']['all_user'] = users_res

        vendor_res = []
        for vendors in all_vendor:
            for users in all_user:
                if vendors.contactor.username == users.username:
                    v = {}
                    v['id'] = vendors.id
                    v['contactor'] = vendors.contactor.username
                    v['company'] = vendors.company
                    v['company_num'] = vendors.company_num
                    v['contact_name'] = vendors.contact_name
                    v['contact_tel'] = vendors.contact_tel
                    v['contact_phone'] = users.phone
                    v['contact_email'] = users.email
                    v['create_time'] = vendors.create_time.strftime("%Y-%m-%d")
                    vendor_res.append(v)
        result['data']['all_vendor'] = vendor_res

        order_res = []
        for orders in all_order:
            o = {}
            o['order_num'] = orders.order_num
            o['ordername'] = orders.ordername
            o['name'] = orders.name
            o['phone'] = orders.phone
            o['addr'] = orders.addr
            o['total_amount'] = format(orders.total_amount,',')
            o["order_item"] = []
            o['create_time'] = orders.create_time.strftime("%Y-%m-%d")
            # 獲取訂單品項---儲存在訂單下層
            order_items = OrderItems.objects.filter(order_num_id=orders.order_num)
            for ot in order_items:
                t = {}
                t['item_name'] = ot.item_name
                t['item_size'] = ot.item_size
                t['item_price'] = format(ot.item_price,',')
                t['item_num'] = ot.item_num
                o["order_item"].append(t)
            order_res.append(o)
        result['data']['all_order'] = order_res

        item_res = []
        for items in all_item:
            i = {}
            i['id'] = items.id
            i['item_name'] = items.item_name
            i['item_num'] = items.item_num
            i['price'] = format(items.price,',')
            i['pic'] = str(items.pic)
            i['item_class'] = items.item_class
            i['vendor'] = items.vendor.company
            i['item_amount'] = items.item_amount
            i['create_time'] = items.create_time
            i['upload_time'] = items.upload_time
            item_res.append(i)
        result['data']['all_item'] = item_res

        return JsonResponse(result)

    @method_decorator(logging_check)
    # /manager/edit_item ----->修改商品
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
        item_ven = json_obj['item_vendor']

        # 檢查price,amount是否為數字
        try:
            int(item_price) and int(item_amount)
        except Exception as e:
            result = {'code': 10309, 'error': '商品資訊輸入錯誤！！'}
            return JsonResponse(result)

        # 檢查表單是否為空
        for a in json_obj.values():
            if not a:
                result = {'code': 10310, 'error': '表單不能為空'}
                return JsonResponse(result)
        # 檢查vendor是否存在
        try:
            vendor = VendorProfile.objects.get(company=item_ven)
        except Exception as e:
            result = {'code': 10311, 'error': '廠商資訊輸入錯誤！！'}
            return JsonResponse(result)
        # 修改商品數據庫
        try:
            edit_item = ItemProfile.objects.get(id=item_id)
        except Exception as e:
            result = {'code': 10312, 'error': '商品不存在！！'}
            return JsonResponse(result)

        edit_item.item_num = item_num
        edit_item.item_name = item_name
        edit_item.price = item_price
        edit_item.item_amount = item_amount
        edit_item.item_class = item_class
        edit_item.vendor_id = vendor.id
        edit_item.save()

        result = {'code': 200}
        return JsonResponse(result)

    @method_decorator(logging_check)
    # /manager/add_item ----->新增商品
    def post(self,request):
        json_str = request.body
        json_obj = json.loads(json_str)
        item_num = json_obj['item_num']
        item_name = json_obj['item_name']
        item_price = json_obj['item_price']
        item_amount = json_obj['item_amount']
        item_class = json_obj['item_class']
        item_vendor = json_obj['item_vendor']
        # 檢查price,amount是否為數字
        try:
            int(item_price) and int(item_amount)
        except Exception as e:
            result = {'code':10313,'error':'商品資訊輸入錯誤！！'}
            return JsonResponse(result)
        # 檢查表單是否為空
        for a in json_obj.values():
            if not a:
                result = {'code': 10314, 'error': '表單不能為空'}
                return JsonResponse(result)
        # 檢查vendor是否存在
        try:
            vendor = VendorProfile.objects.get(company=item_vendor)
        except Exception as e:
            result = {'code': 10315, 'error': '廠商資訊輸入錯誤！！'}
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
        add_item.vendor_id = vendor.id
        add_item.save()

        result = {'code': 200}
        return JsonResponse(result)