from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.

def post_index(request):
    qs_list = Post.objects.all()
    paginator = Paginator(qs_list, 5)
    page_request_var = 'page'
    page_number = request.GET.get(page_request_var)
    page_obj = paginator.get_page(page_number)
    context = {'queryset':page_obj,'title':'List of Posts','page_request_var':page_request_var}
    return render(request,template_name='posts/index.html',context=context)

def post_create(request):
    if not request.user.is_authenticated:
        return HttpResponse('You are not authenticated')
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,'Post created.')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {'form':form}
    return render(request,template_name='posts/create.html',context=context)

def post_list(request):
    if not request.user.is_authenticated:
        return HttpResponse('You are not authenticated')
    qs_list = Post.objects.filter(user=request.user)
    paginator = Paginator(qs_list, 5)
    page_request_var = 'page'
    page_number = request.GET.get(page_request_var)
    page_obj = paginator.get_page(page_number)
    context = {'queryset':page_obj,'title':'List of Posts','page_request_var':page_request_var}
    return render(request,template_name='posts/list.html',context=context)

def post_details(request,slug=None):
    qs_details = get_object_or_404(Post,slug=slug)
    if qs_details.draft or qs_details.publish > timezone.now().date():
        if not request.user.is_authenticated:
            return HttpResponse('You are not authenticated')
    context = {'query':qs_details,'title':qs_details.title}
    return render(request,template_name='posts/details.html',context=context)

def post_update(request,slug=None):
    qs_update = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None,request.FILES or None,instance=qs_update)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {'query':qs_update,'title':qs_update.title,'form':form}
    return render(request,template_name='posts/edit.html',context=context)

def post_delete(request,slug=None):
    qs_delete = get_object_or_404(Post,slug=slug)
    qs_delete.delete()
    messages.success(request,'Succesfully deleted.')
    return HttpResponseRedirect(reverse('posts:postlist'))

def contact(request):
    return render(request,template_name='posts/contact.html')
    