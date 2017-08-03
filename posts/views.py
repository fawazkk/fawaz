
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from urllib.parse import quote
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
	obj_list = Post.objects.all().order_by("-timestamp","-updated")

	paginator = Paginator(obj_list, 5) # Show 5 contacts per page
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
		"user": request.user
	}
	return render(request, 'post_list.html', context)
	
def post_detail(request, post_slug):
	obj = get_object_or_404(Post, slug=post_slug)
	context = {
		"instance": obj,
		"share_string": quote(obj.content)
		}

	return render (request, 'post_detail.html', context)


def post_create(request):
	form = PostForm(request.POST or None,request.FILES or None)
 
	if form.is_valid():
		form.save()
		messages.success(request, "OMG! So cool! you created an object.")
		return redirect("posts:list")
	context = {
	"title": "Create",
	"form": form,

	}
	return render(request, 'post_create.html', context)


def post_update(request,slug=post_slug):
	instance = get_object_or_404(Post, slug=post_slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		form.save()
		messages.success(request, "Successfully updated!")
		return redirect("posts:list")
	context = {
	"title": "Update",
	"form": form,
	}
	return render(request, 'post_update.html', context)


def post_delete(request, post_slug):
	obj=Post.objects.get(slug=post_slug).delete()
	messages.warning(request, "Steve Jobs says hi!")
	return redirect("posts:list")


