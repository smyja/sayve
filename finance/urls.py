from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from escrow.views import home_view, signup_view,login_view, dashboard, activation_sent_view, activate,logout_user
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_user, name = 'logout'),
    path('dashboard/', dashboard, name="dashboard"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]