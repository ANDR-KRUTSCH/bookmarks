from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST

from actions.utils import create_action
from actions.models import Action
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact

# Create your views here.
@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('pk', flat=True)
    if following_ids:
        actions = actions.filter(user__pk__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    context = dict(
        section='dashboard',
        actions=actions,
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
            create_action(user=new_user, verb='has created an account')

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
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request=request, message='Profile updated successfully')
        else:
            messages.error(request=request, message='Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = dict(
        user_form=user_form,
        profile_form=profile_form,
    )

    return render(request=request, template_name='account/edit.html', context=context)

@login_required
def user_list(request: HttpRequest) -> HttpResponse:
    users = User.objects.filter(is_active=True)

    context = dict(
        section='people',
        users=users,
    )

    return render(request=request, template_name='account/users/list.html', context=context)

def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(klass=User, username=username, is_active=True)
    
    context = dict(
        section='people',
        user=user,
    )

    return render(request=request, template_name='account/users/detail.html', context=context)

@login_required
@require_POST
def user_follow(request: HttpRequest) -> JsonResponse:
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(pk=user_id)
            if request.user not in user.followers.all():
                Contact.objects.create(user_from=request.user, user_to=user)
                create_action(user=request.user, verb='is following', target=user)
            else:
                Contact.objects.filter(from_user=request.user, to_user=user).delete()
            return JsonResponse(data=dict(status='ok'))
        except User.DoesNotExist:
            pass
    return JsonResponse(data=dict(status='error'))

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