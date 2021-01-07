from django.shortcuts import render,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
import logging
import logging.config


from .models import Comment
from .forms import CommentForm

# Create your views here.

logging.config.fileConfig(fname='logs/log.conf')
logger = logging.getLogger('comments')

def comment_delete(request,id):
    try:
        comment_delete = Comment.objects.get(id=id)
    except:
        raise Http404('This is not present')

    if comment_delete.user != request.user:
        response = HttpResponse("you dont have permission to view this.")
        response.status_code = 403
        return response

    if request.method == 'POST':
        parent_object_url = comment_delete.content_object.get_absolute_url()
        logger.info(f'{request.user} deleted {comment_delete.content}')
        comment_delete.delete()
        messages.success(request,'Comment has been deleted')
        return HttpResponseRedirect(parent_object_url)
    context = {'comment_delete':comment_delete}
    return render(request,'comments/comment_delete.html',context=context)

def comment_thread(request,id):
    try:
        comment = get_object_or_404(Comment,id=id)
    except:
        raise Http404

    if not comment.is_parent:
        obj = obj.parent

    content_object = comment.content_object
    object_id = comment.content_object.id

    initial_data = {
            "content_type": comment.content_type,
            "object_id": comment.object_id
    }

    form = CommentForm(request.POST or None,initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type = form.cleaned_data.get("content_type")
        app_label,model_label = c_type.split('|')
        content_type = ContentType.objects.get(app_label__iexact=app_label.strip(), model__iexact=model_label.strip())
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment,created = Comment.objects.get_or_create(
                                    user = request.user,
                                    content_type = content_type,
                                    object_id = obj_id,
                                    content =content_data,
                                    parent = parent_obj,
        )
        logger.info(f'{request.user} commented {new_comment.content}.')
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context = {'comment':comment,'form':form}
    return render(request,'comments/comment_thread.html',context=context)
