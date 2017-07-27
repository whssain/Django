from django.shortcuts import render , redirect
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
"""def post_create(request):
	post_list = Post.objects.all()
	post_filter = Post.objects.filter(title='Noor')
	post_get = Post.objects.get(title = "gf")
	context={
	"user": request.user,
	"list": post_list,
	"filter": post_filter,
	get": post_get

	#"random_number":random.re
    
	}
	 return render(request,'create.html',context) """

def post_detail(request ,post_id):
	obj=get_object_or_404(Post, id=post_id)
	context ={
	"instance":obj,
	}
	return render(request,'post_detail.html',context)

def post_list(request):
    object_list = Post.objects.all() #.order_by("-timestamp","-updated")

    paginator = Paginator(object_list, 2) # Show 5 contacts per page
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
    "object_list": objects,
    "title": "List",
    "user": request.user
    }
    return render(request, 'post_list.html', context)
def post_create(request):
	form = PostForm(request.POST or None , request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request,"OMG! So Cool!")
		return redirect ("posts:list")
	context = {
		"form":form
	}
	return render(request,'post_create.html',context)


def post_update(request,post_id):
	post_object = get_object_or_404(Post , id=post_id)
	form = PostForm(request.POST or None , request.FILES or None ,instance=post_object)
	if form.is_valid():
		form.save()
		#messages.success(request,"Giving it a second thought?")
		return redirect ("posts:list")
	context = {
		"form":form,
		"post_object":post_object,
	}
	return render(request,'post_update.html',context)

def post_delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	messages.warning(request ,"Seriously bro?")
	return redirect ("posts:list")
	
