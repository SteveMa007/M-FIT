from django.urls import path

from ibackstage import views

urlpatterns = [
    path('del_user',views.del_user),
    path('del_vendor',views.del_vendor),
    path('del_item',views.del_item),
    path('add_item_pic',views.add_item_pic),
    path('add_item',views.ManagerViews.as_view()),
    path('edit_item',views.ManagerViews.as_view()),
]