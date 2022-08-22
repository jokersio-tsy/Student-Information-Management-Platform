"""djangoProject3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/hello/<str:name>', views.hello),
    path('app/getTeacherInfo/', views.getTeacherInfo),
    path('app/add_data_student/', views.add_data_student),
    path('app/gotoinformation_getter_web/', views.gotoinformation_getter_web),
    path('app/ajax/picupload/', views.picupload),
    path('app/queryAll/', views.queryAll),
    path('app/queryByCondition/', views.queryByCondition),
    path('app/preUpdate/<int:stu_id>', views.preUpdate),
    path('app/update/', views.update),
    path('app/delete/<int:stu_id>', views.delete),
    path('app/makeqrcode/', views.makeqrcode),
    path('app/register/', views.register),
    path('app/homepage/', views.homepage),
    path('app/login/', views.login),
    path('app/logout/', views.logout),
    path('app/gotosendemail/', views.gotosendemail),
    path('app/sendEmail/', views.sendEmail),
    path('app/testEmail/', views.testEmail),
    path('app/makeCovid/', views.makeCovid),
    path('app/getconfirm/', views.get_confirm),
    path('app/setRisk/', views.setRisk),
    path('app/queryRisk/', views.queryRisk),
    path('app/gotoepidemic_ctrl/', views.gotoepidemic_ctrl),
    
]
