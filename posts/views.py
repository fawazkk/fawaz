
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from urllib.parse import quote
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.utils import timezone
from django.db.models import Q

def post_list(request):
    today = timezone.now().date()
    object_list = Post.objects.filter(draft=False).filter(publish__lte=today)
    if request.user.is_staff or request.user.is_superuser:
        object_list = Post.objects.all()

        query = request.GET.get("q")
    if query:
        object_list = object_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(author__first_name__icontains=query)|
            Q(author__last_name__icontains=query)
            ).distinct()




    paginator = Paginator(object_list, 5) # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)


    context = {
        "post_list": objects,
        "title": "List",
        "user": request.user,
        "today": today,
    }
    return render(request, 'post_list.html', context)
    
def post_detail(request, post_slug):
    obj = get_object_or_404(Post, slug=post_slug)
    if obj.publish>timezone.now().date() or obj .draft:
        if not (request.user.is_staff or request.user.is_superuser):
            raise Http404


    context = {
        "instance": obj,
        "share_string": quote(obj.content)
        }

    return render (request, 'post_detail.html', context)


def post_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    form = PostForm(request.POST or None,request.FILES or None)
 
    if form.is_valid():
        post = form.save(commit = False)
        post.author = request.user
        post.save()
        messages.success(request, "Successfully Created!")
        return redirect("posts:list")
    context = {
    "title": "Create",
    "form": form,

    }
    return render(request, 'post_create.html', context)


def post_update(request,post_slug):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    instance = get_object_or_404(Post, slug=post_slug)
    form = PostForm(request.POST or None, request.FILES or None, instance = instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated!")
        return redirect("posts:list")
    context = {
    "title": "Update",
    "form": form,
    "instance":instance,
    }
    return render(request, 'post_update.html', context)


def post_delete(request, post_slug):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    obj=Post.objects.get(slug=post_slug).delete()
    messages.warning(request, "Steve Jobs says hi!")
    return redirect("posts:list")


