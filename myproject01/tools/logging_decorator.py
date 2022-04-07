import jwt
from django.conf import settings
from django.http import JsonResponse
from users.models import UserProfile


def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 獲取請求頭AUTHORIZATION
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code':403,'error':'請登入！！'}
            return JsonResponse(result)
        # 驗證token
        key = settings.JWT_TOKEN_KEY
        try:
            token_check = jwt.decode(token,key,algorithms='HS256')
        except Exception as e:
            print('jwt decode error is %s'%(e))
            result = {'code': 403, 'error': '請登入'}
            return JsonResponse(result)
        # 獲取登入用戶
        username = token_check['username']
        user = UserProfile.objects.get(username=username)
        # 查看用戶是否啟用
        if user.active != True:
            result = {'code':403,'error':'此用戶不存在！！'}
            return JsonResponse(result)
        request.logging_user = user

        return func(request, *args, **kwargs)
    return wrap