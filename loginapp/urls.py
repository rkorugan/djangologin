from django.conf.urls import url
from loginapp import views

#app_name = 'loginapp'

urlpatterns=[
url(r'^register/$',views.register,name='register'),
url(r'^user_login/$',views.user_login,name='login')

]