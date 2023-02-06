from django.urls import path, include
from . import views

urlpatterns= [
    path('', views.post_list, name='post_list'),
    path('VR/',views.VR, name='VR'),

    path('post/<int:pk>/',views.post_detail, name='post_detail'),
    path('post/new/',views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),

    path('logout/',views.logout_request, name='logout'),
    path('signup/',views.sign_up, name='sign_up'),
    path('profile/<int:pk>/',views.profile_edit,name='profile_edit'),
]