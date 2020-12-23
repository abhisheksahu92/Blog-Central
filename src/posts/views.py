from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import PostForm

# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(reverse('posts:postlist'))
    context = {'form':form}
    return render(request,template_name='posts/create.html',context=context)

def post_list(request):
    qs_list = Post.objects.all()
    context = {'queryset':qs_list,'title':'List of Posts'}
    return render(request,template_name='posts/list.html',context=context)

def post_details(request,id=None):
    qs_details = get_object_or_404(Post,id=id)
    context = {'query':qs_details,'title':qs_details.title}
    return render(request,template_name='posts/details.html',context=context)

def post_update(request,id=None):
    qs_update = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,instance=qs_update)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(reverse('posts:postlist'))
    context = {'query':qs_update,'title':qs_update.title,'form':form}
    return render(request,template_name='posts/edit.html',context=context)

def post_delete(request):
    return HttpResponse('<h1>Delete</h1<')