from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('add/', views.create_order_view, name='add'),
    path('data/', views.VoteUpPost.as_view(), name='view-data')
]