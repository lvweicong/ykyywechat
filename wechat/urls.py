from django.conf.urls import url,include

from . import views

app_name = 'wechat'

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.weixin_main, name='weixin_main'),
    #url(r'^startmymenu$', views.startmymenu, name='startmymenu'),
    ]