from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Post
from .forms import PostForm

from comments.models import Comment
from comments.forms import CommentForm


# Create your views here.

def post_index(request):
    qs_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        qs_list = qs_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
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
    query = request.GET.get("q")
    if query:
        qs_list = qs_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
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
    initial_data = {'content_type':qs_details.get_content_type,'object_id':qs_details.id}
    form = CommentForm(request.POST or None,initial=initial_data)
    if form.is_valid():
        print(form.cleaned_data)
        c_type = form.cleaned_data.get("content_type")
        app_label,model_label = c_type.split('|')
        content_type = ContentType.objects.get(app_label__iexact=app_label.strip(), model__iexact=model_label.strip())
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        new_comment,created = Comment.objects.get_or_create(
                                    user = request.user,
                                    content_type = content_type,
                                    object_id = obj_id,
                                    content =content_data
        )

    comments = qs_details.comment
    context = {'query':qs_details,'title':qs_details.title,'comments':comments,'comment_form':form}
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
    