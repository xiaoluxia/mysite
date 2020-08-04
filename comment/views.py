from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
#使用这个模型可以解决很多的输入内容不相符的问题
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

def updata_comment(request):
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    comment_form = CommentForm(request.POST,user= request.user)
    data = {}

    if comment_form.is_valid():
            #检查通过
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
#获取类型和id的类型，使用contenttype的方法。

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #返回数据        
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['comment_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['id'] = comment.id
        data['root_id'] = comment.root.id if not comment.root is None else ''

    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors)[0][0]
    return JsonResponse(data)
        #return render(request, 'error.html', {'message': comment_form.errors,'redirect_to':referer})




