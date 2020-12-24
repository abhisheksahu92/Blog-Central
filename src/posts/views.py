from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm

# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Post created.')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {'form':form}
    return render(request,template_name='posts/create.html',context=context)

def post_list(request):
    qs_list = Post.objects.all()
    paginator = Paginator(qs_list, 5)
    page_request_var = 'page'
    page_number = request.GET.get(page_request_var)
    page_obj = paginator.get_page(page_number)
    context = {'queryset':page_obj,'title':'List of Posts','page_request_var':page_request_var}
    return render(request,template_name='posts/list.html',context=context)

def post_details(request,id=None):
    qs_details = get_object_or_404(Post,id=id)
    context = {'query':qs_details,'title':qs_details.title}
    messages.success(request,'Post Saved.')
    return render(request,template_name='posts/details.html',context=context)

def post_update(request,id=None):
    qs_update = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,request.DATA or None,instance=qs_update)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {'query':qs_update,'title':qs_update.title,'form':form}
    return render(request,template_name='posts/edit.html',context=context)

def post_delete(request,id=None):
    qs_update = get_object_or_404(Post,id=id)
    qs_update.delete()
    messages.success(request,'Succesfully deleted.')
    return HttpResponseRedirect(reverse('posts:postlist'))
    