from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from .models import Blog, BlogType
from read_statistic.utils import read_statistic_once_read
from mysite.forms import LoginForm

def blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) #每十页进行分页
    page_num = request.GET.get('page', 1)# 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) #自动判断输入的是否是整数以及处理
    current_page_num = page_of_blogs.number #获取当前页码
    #获取当前页码的前后两页
    page_range = list(range(max(current_page_num -2,1),current_page_num))+\
                 list(range(current_page_num,min(paginator.num_pages,current_page_num + 2)+1))
    #加上省略页
    if page_range[0] -1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    #显示第一和最后一页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

     #获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time','month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    
    blogs_all_list =  Blog.objects.all()
    context = blog_list_common_data(request,blogs_all_list)
    return render(request,'blog/blog_list.html',context)

def blogs_with_type(request, blog_type_id):
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    blogs_all_list =  Blog.objects.filter(blog_type=blog_type)
    context = blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_with_type.html', context)

def blogs_with_date(request, year,month):
    blogs_all_list =  Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = blog_list_common_data(request,blogs_all_list)
    context['bolgs_with_date'] = '%s年%s月' % (year,month)
    return render(request,'blog/blogs_with_date.html', context)

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    read_cookie_key = read_statistic_once_read(request,blog)
  
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['login_form'] = LoginForm()
    response = render(request,'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key,'ture')#阅读的标记
    return response



# Create your views here.
