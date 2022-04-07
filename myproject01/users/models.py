from django.db import models
# from items.models import ItemProfile

# Create your models here.

# 使用者
class UserProfile(models.Model):
    PERMISSION=(
        ('user', 'user'),
        ('vendor', 'vendor'),
        ('manager', 'manager')
    )
    username = models.CharField('帳號',max_length=16,primary_key=True)
    userpwd = models.CharField('密碼',max_length=32)
    name = models.CharField('姓名',max_length=20,null=True)
    email = models.EmailField('電子信箱')
    phone = models.CharField('手機',max_length=10)
    addr = models.CharField('地址',max_length=100,default='--尚無設定地址--')
    amount = models.IntegerField('消費金額',default=0)
    permission = models.CharField('權限',max_length=7,default='user',choices=PERMISSION)
    create_time = models.DateField('註冊日期',auto_now_add=True)
    upload_time = models.DateField('更新日期',auto_now=True)
    active = models.BooleanField('是否使用',default=1)

    class Meta:
        db_table = 'users_user_profile'
        verbose_name_plural = '使用者資訊'

        def __str__(self):
            return '帳號：{},{},信箱：{},手機：{},{},消費金額：{},權限：{},註冊日期：{},更新日期：{},啟用：{}'.format(self.username,self.userpwd,self.email,self.phone,self.addr,self.amount,self.permission,self.create_time,self.upload_time,self.active)

# 廠商
class VendorProfile(models.Model):
    contactor = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    company = models.CharField('公司',max_length=50)
    company_num = models.CharField('統一編號',max_length=8)
    contact_name = models.CharField('聯絡人',max_length=10)
    contact_tel = models.CharField('公司電話',max_length=20)
    create_time = models.DateField('合作日期', auto_now_add=True)
    upload_time = models.DateField('更新日期', auto_now=True)
    active = models.BooleanField('是否使用', default=1)

    class Meta:
        db_table = 'users_vendor_profile'
        verbose_name_plural = '廠商資訊'

        def __str__(self):
            return '聯絡窗口：{},公司：{},統一編號：{},聯絡人：{},電話：{},手機：{},信箱：{},合作日期：{},更新日期{},啟用{}'.format(self.contactor,self.company,self.company_num,self.contact_name,self.contact_tel,self.contact_phone,self.contact_email,self.create_time,self.upload_time,self.active)

# 歷史訂單
class HistoryOrder(models.Model):
    order_num = models.CharField('訂單編號',max_length=12,primary_key=True) # xxxxooabcdef
    ordername = models.CharField('帳號',max_length=20,null=True)
    name = models.CharField('姓名',max_length=16)
    total_amount = models.IntegerField('總金額')
    phone = models.CharField('手機',max_length=10)
    email = models.EmailField('電子信箱')
    addr = models.CharField('配送地址',max_length=100)
    paypal_id = models.CharField('PayPal訂單編號',max_length=255)
    status = models.BooleanField('訂單狀態', default=0)
    create_time = models.DateField('購買日期', auto_now_add=True)

    class Meta:
        db_table = 'users_history_order'
        verbose_name_plural = '歷史訂單'

        def __str__(self):
            return '訂單編號：{},訂購人：{},總金額：{},購買日期：{}'.format(self.order_num,self.ordername,self.total_amount,self.create_time)

# 訂單品項
class OrderItems(models.Model):
    order_num = models.ForeignKey(HistoryOrder,on_delete=models.CASCADE)
    item_name = models.CharField('訂購商品', max_length=50)
    item_size = models.CharField('商品尺寸',max_length=10)
    item_price = models.IntegerField('商品價格')  # 商品可能後續不供應，故直接紀錄
    item_num = models.IntegerField('訂購數量')  # 可能有價格變動問題，故直接紀錄

    class Meta:
        db_table = 'users_order_items'
        verbose_name_plural = '訂單品項'

        def __str__(self):
            return '訂單編號：{},訂購商品：{},尺寸：{},價格：{},數量：{}'.format(self.order_num,self.item_name,self.item_size,self.item_price,self.item_num)


