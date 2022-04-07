"""myproject01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from users import views as users_views
from ibackstage import views as ibackstage_views
from itoken import views as itoken_views
from items import views as items_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/manager_backstage', ibackstage_views.ManagerViews.as_view()),
    path('v1/manager/', include('ibackstage.urls')),
    path('v1/users', users_views.UserViews.as_view()),
    path('v1/users/', include('users.urls')),
    path('v1/vendor/', include('users.urls')),
    path('v1/itoken', itoken_views.tokens),
    path('v1/index', items_views.ItemViews.as_view()),
    path('v1/index/cart', items_views.CartViews.as_view()),
    path('v1/index/cart/update', items_views.CartViews.as_view()),
    path('v1/check_out', items_views.check_out),
    path('v1/search', items_views.search_view),
    path('v1/item/<int:item_id>', items_views.item_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
