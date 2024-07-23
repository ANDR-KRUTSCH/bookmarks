from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.
@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    context = dict(
        section='dashboard',
    )

    return render(request=request, template_name='account/dashboard.html', context=context)

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user: User = form.save(commit=False)
            new_user.set_password(raw_password=form.cleaned_data.get('password'))
            new_user.save()
            Profile.objects.create(user=new_user)

            context = dict(
                new_user=new_user,
            )

            return render(request=request, template_name='account/register_done.html', context=context)
    else:
        form = UserRegistrationForm()

    context = dict(
        form=form,
    )

    return render(request=request, template_name='account/register.html', context=context)

@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = dict(
        user_form=user_form,
        profile_form=profile_form,
    )

    return render(request=request, template_name='account/edit.html', context=context)


# def user_login(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request=request, username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request=request, user=user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()

#     context = dict(
#         form=form,
#     )

#     return render(request=request, template_name='account/login.html', context=context)