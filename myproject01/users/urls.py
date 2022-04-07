from django.urls import path
from users import views
from items import views as item_views

urlpatterns = [
    path('change_pwd',views.UserViews.as_view()),
    path('center',views.UserViews.as_view()),
    path('change_addr',views.user_views),
    path('add_favor',views.add_favor),
    path('del_favor',views.del_favor),
    path('score_item',views.score_item),
    # vendor
    path('register', views.VendorViews.as_view()),
    path('products', views.VendorViews.as_view()),
    path('del_item', views.VendorViews.as_view()),
    path('edit_item', views.VendorViews.as_view()),
    path('add_item', views.add_item),
    path('add_item_pic', views.add_item_pic),

]