from django.urls import path

from . import views

app_name = 'images'

urlpatterns = (
    path(route='create/', view=views.image_create, name='create'),
    path(route='detail/<int:pk>/<slug:slug>/', view=views.image_detail, name='detail'),
    path(route='like/', view=views.image_like, name='like'),
    path(route='', view=views.image_list, name='list'),
)