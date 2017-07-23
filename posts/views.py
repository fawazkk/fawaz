from django.shortcuts import render
from django.http import HttpResponse

def post_create(request):
	post_list = Post.objects.all()
	Post_kkk=Post.objects.all().first()
	contest = {
		'user': request.user,
		'list': post_list,
		'obj' : Post_kkk
	}
	return render(request, 'create.html', context)
	
