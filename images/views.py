from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ImageCreateForm
from .models import Image

# Create your views here.
@login_required
def image_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request=request, message='Image added successfully')
            redirect(image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    context = dict(
        section='images',
        form=form,
    )

    return render(request=request, template_name='images/image/create.html', context=context)

def image_detail(request: HttpRequest, pk: int, slug: str) -> HttpResponse:
    image = get_object_or_404(klass=Image, pk=pk, slug=slug)

    context = dict(
        section='images',
        image=image,
    )

    return render(request=request, template_name='images/image/detail.html', context=context)

@login_required
@require_POST
def image_like(request: HttpRequest) -> JsonResponse:
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(pk=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse(dict(status='ok'))
        except Image.DoesNotExist:
            pass
    return JsonResponse(dict(status='error'))

@login_required
def image_list(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    
    images = Image.objects.all()

    paginator = Paginator(object_list=images, per_page=8)

    try:
        images = paginator.page(number=page)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(number=paginator.num_pages)
    except PageNotAnInteger:
        images = paginator.page(number=1)

    context = dict(
        section='images',
        images=images,
    )

    if images_only:
        return render(request=request, template_name='images/image/list_images.html', context=context)
    
    return render(request=request, template_name='images/image/list.html', context=context)