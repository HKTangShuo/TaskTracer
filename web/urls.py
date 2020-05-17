from django.conf.urls import url

from web.views import account

urlpatterns = [

    url('test', account.test)
]
