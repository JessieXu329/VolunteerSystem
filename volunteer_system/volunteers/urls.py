from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_list, name='activity_list'),
    path('api/activities/', views.activity_list_api, name='activity_list_api'),
    path('api/activities/<int:activity_id>/', views.activity_detail_api, name='activity_detail_api'),
    path('api/activities/<int:activity_id>/signup/', views.volunteer_signup, name='volunteer_signup'),
]