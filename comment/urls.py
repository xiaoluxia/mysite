from django.urls import path
from .import views

#start with blog
urlpatterns = [
    # http://localhost:8000/blog/1
    path('updata_comment', views.updata_comment, name='updata_comment'),
]