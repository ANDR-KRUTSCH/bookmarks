from django.urls import path, include
from django.contrib.auth import urls
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = (
    # path(route='login/', view=views.user_login, name='login'),

    # path(route='login/', view=auth_views.LoginView.as_view(), name='login'),
    # path(route='logout/', view=auth_views.LogoutView.as_view(), name='logout'),
    # path(route='password-change/', view=auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path(route='password-change/done/', view=auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path(route='password_reset/', view=auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path(route="password_reset/done/", view=auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path(route="reset/<uidb64>/<token>/", view=auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path(route="reset/done/", view=auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path(route='', view=include(arg='django.contrib.auth.urls')),
    path(route='', view=views.dashboard, name='dashboard'),
    path(route='register/', view=views.register, name='register'),
    path(route='edit/', view=views.edit, name='edit'),
    path(route='users/', view=views.user_list, name='user_list'),
    path(route='users/follow/', view=views.user_follow, name='user_follow'),
    path(route='users/<username>/', view=views.user_detail, name='user_detail'),
)