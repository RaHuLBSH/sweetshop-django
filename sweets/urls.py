from django.urls import path

from . import views

urlpatterns=[
    path('login/',views.login_view, name='login'),
    path('register/',views.register_view, name='register'),
    path('homepage/',views.home, name="home"),
    path('_admin/',views.admin,name="_admin"),
    path('homepage/<str:state>/',views.homepage, name='homepage'),
    path('user/',views.user,name="user"),
    path('homepage/<str:state>/info/',views.blog, name='blog'),
    path('goto_cw/<str:cw>',views.goto_cw,name="goto_cw"),
    path('addmoney/',views.addmoney,name='addmoney'),
    path('addm',views.addm,name="addm"),
    path('homepage/goto_cw/<str:cw>',views.goto_cw,name="goto_cw"),
    path('add_cw/<str:pname>',views.add_cw,name="add_cw"),
    path('remove_cw/<str:pname>/<str:cw>',views.remove_cw,name="remove_cw"),
    path('order',views.order,name='order'),
    path('placeorder/<int:gtotal>',views.placeorder,name="placeorder"),
    path('myorders/',views.myorders,name="myorders"),
    path('showbill/<int:id>',views.showbill,name="showbill"),
    path('download/<int:id>',views.download,name="download"),
    path('update_product/<str:pname>',views.update_product,name="update_product"),
    path('update_status/<int:id>',views.update_status,name="update_status"),
    path('add_review',views.add_review,name="add_review"),
    path('add_blogreview/<str:state>',views.add_blogreview,name="add_blogreview"),
]