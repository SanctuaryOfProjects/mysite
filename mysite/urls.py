"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from delivery.views import *

urlpatterns = [
    path('', index, name='index'),
    path('est/', est_list, name='est'),
    path('est/<int:establishment_id>/',establishment_detail , name='establishment_detail'),
    path('est/delete/<int:pk>/', delete_est, name='est_delete'),
    path('couriers/', couriers, name='couriers'),
    path('couriers/delete/<int:pk>/', delete_courier, name='cours_delete'),
    path('orders/<int:order_id>/route/', show_route_map, name='show_route_map'),
    path('orders/', order, name='orders'),
    path('orders/<int:order_id>/delete/', delete_order, name='delete_order'),
    path('schedule/', schedule, name='schedule'),
    path('schedule/<int:establishment_id>/', view_schedule, name='view_schedule'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('setsalary/', salary_calculator, name='setsalary'),
    path('inprogress/', in_progress_orders, name='inprogress'),

    path('dashboard/', dashboard, name='dashboard'),
    path('accept_order/<int:order_id>/', accept_order, name='accept_order'),
    path('myorders/', myorders, name='myorders'),
    path('mysalary/', mysalary, name='mysalary'),
    path('myestablishments', courier_establishments, name='myest'),
    path('myschedule/', courier_schedule, name='myschedule'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]


