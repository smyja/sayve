from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from escrow.views import home_view, webhook_logs,signup_view,login_view, transfer,dashboard,buycoins,verifybvn, activation_sent_view, activate,logout_user,webhook
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_user, name = 'logout'),
    path('dashboard/', dashboard, name="dashboard"),
    path('verify/', verifybvn, name="verifybvn"),
    path('send/',transfer, name="transfer"),
    path('webhook/', webhook, name="webhook"),
    path('hook/logs/', webhook_logs, name="webhook_logs"),
    path('buycoins/', buycoins, name="buycoins"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),

]