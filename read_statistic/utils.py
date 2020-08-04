import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail

def read_statistic_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.id)

    if not request.COOKIES.get(key):
        #总阅读数加一
        readnum, created= ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)        
        readnum.read_num += 1
        readnum.save()
        #当天的阅读数加一
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id= obj.id, date=date)       
        readDetail.read_num += 1
        readDetail.save()
    return key

    #为不同类型的数据服务，需要内容的类型作为参数。
def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7,0,-1):
    #时间加减的函数
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
    #得到字典，求和的结果
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return read_details[:7]



