from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
# Create your views here.
def post_create(request):
	post_list = Post.objects.all()
	post_filter = Post.objects.filter(title='Noor')
	post_get = Post.objects.get(title = "gf")
	context={
	"user": request.user,
	"list": post_list,
	"filter": post_filter,
	"get": post_get

	#"random_number":random.re
    
	}
	return render(request,'create.html',context)

def post(request):
	obj=get_object_or_404(Post, id=2)
	context ={
	"instance":obj;
	}
	return render(request,'whatever.html',context)


