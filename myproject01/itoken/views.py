import json
import hashlib
import time
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from tools.make_token import make_token
from users.models import UserProfile
# Create your views here.
def tokens(request):

    if request.method != 'POST':
        result = {'code':10201,'error':'通讯方式错误！！'}
        return JsonResponse(result)

    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    userpwd = json_obj['userpwd']

    # 驗證帳號
    try:
        name = UserProfile.objects.get(username=username)
    except Exception as e:
        result = {'code': 10202, 'error': '帳號或密碼錯誤'}
        return JsonResponse(result)

    # 驗證密碼
    m = hashlib.md5()
    m.update(userpwd.encode())
    if name.userpwd != m.hexdigest():
        result = {'code': 10203, 'error': '帳號或密碼錯誤'}
        return JsonResponse(result)

    # 紀錄登錄狀態
    token = make_token(username)
    result = {'code': 200, 'username':username, 'data':{'token':token}}
    return JsonResponse(result)





