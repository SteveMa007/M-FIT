from django.db import models
from users.models import UserProfile
from users.models import VendorProfile

# Create your models here.

# 商品
class ItemProfile(models.Model):
    ITEM_CLASS = (
        ('外套', '外套'),
        ('帽T', '帽T'),
        ('長袖', '長袖'),
        ('短袖', '短袖'),
        ('背心', '背心'),
        ('長褲', '長褲'),
        ('短褲', '短褲'),
        ('帽子', '帽子'),
        ('襪子', '襪子'),
        ('背包', '背包')
    )
    item_name = models.CharField('名稱',max_length=50)
    item_num = models.CharField('編號',max_length=6)
    price = models.IntegerField('價格')
    pic = models.ImageField('圖片',upload_to='item_pic/')
    item_class = models.CharField('類別',max_length=6,choices=ITEM_CLASS)
    score = models.ManyToManyField(to=UserProfile,through='ScoreItem',related_name='user_score')
    favor = models.ManyToManyField(to=UserProfile,through='FavorItem',related_name='user_favor')
    cart = models.ManyToManyField(to=UserProfile,through='CartItems',related_name='user_cart')
    vendor = models.ForeignKey(to=VendorProfile,on_delete=models.CASCADE)
    item_amount = models.IntegerField('庫存量')
    create_time = models.DateField('上架日期', auto_now_add=True)
    upload_time = models.DateField('更新日期', auto_now=True)
    active = models.BooleanField('是否使用', default=1)


    class Meta:
        db_table = 'items_item_profile'
        verbose_name_plural = '商品資訊'

        def __str__(self):
            return '名稱：{},編號：{},價格：{},{},類別：{},評分：{},廠商：{},庫存：{},上架日期：{},更新日期：{},啟用：{}'.format(self.item_name,self.item_num,self.price,self.pic,self.item_class,self.score,self.vendor,self.item_amount,self.create_time,self.upload_time,self.active)

# 收藏清單
class FavorItem(models.Model):
    username = models.ForeignKey(to=UserProfile,on_delete=models.CASCADE)
    itemname = models.ForeignKey(to=ItemProfile,on_delete=models.CASCADE)
    upload_time = models.DateField('收藏日期', auto_now=True)
    active = models.BooleanField('是否使用', default=1)

    class Meta:
        db_table = 'users_favor_items'
        verbose_name_plural = '收藏清單'

        def __str__(self):
            return '帳號：{},商品：{},收藏日期：{},啟用：{}'.format(self.username,self.itemname,self.upload_time,self.active)

# 評分
class ScoreItem(models.Model):
    username = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(to=ItemProfile, on_delete=models.CASCADE)
    item_score = models.IntegerField('評分')
    upload_time = models.DateField('評分日期', auto_now=True)
    active = models.BooleanField('是否使用', default=1)

    class Meta:
        db_table = 'users_score_items'
        verbose_name_plural = '評分清單'

        def __str__(self):
            return '帳號：{},商品：{},評分：{},評分日期：{},啟用：{}'.format(self.username,self.itemname,self.item_score,self.upload_time,self.active)

# 購物車
class CartItems(models.Model):
    order_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item_name = models.ForeignKey(ItemProfile, on_delete=models.CASCADE)
    item_size = models.CharField('商品尺寸', max_length=10)
    item_num = models.IntegerField('訂購數量')
    create_time = models.DateField('加入日期', auto_now_add=True)

    class Meta:
        db_table = 'users_cart_items'
        verbose_name_plural = '購物車'

        def __str__(self):
            return '顧客：{},商品：{},尺寸：{},數量：{},加入日期：{}'.format(self.order_name,self.item_name,self.item_size,self.item_num,self.create_time)