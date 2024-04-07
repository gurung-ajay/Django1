"""
URL configuration for blogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
# import views from boards app
from boards import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # when empty sub url is given, it set to open home function from views
    path('', views.home, name='home'),
    
    # same as above but using regex
    # re_path(r'^$', views.home, name='home')
    
    # regex path. boards is static but this part((?P<pk>\d+)) means it can have any value such as ip/boards/1, ip/boards/2, etc
    # which will be passed as primary key for board model (see board_topics views for more detail)
    re_path(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    
    # url link for about page
    re_path(r'^about/$', views.about, name='about'),
    # alternative: using path
    # path('/about/', views.about, name='about'),
    
    # ?P assigns variables to <var>
    # \d means digit 0-9, + means one or more occurences
    re_path(r'^questions/(?P<pk>\d+)/$', views.question, name='question'),
    # - means you can insert - sign in that sub-url section, /w  means only char a-z, A-Z, 0-9 
    # if - is not stated, you can write 'helloworld' but not 'hello-world' as - will not be supported
    re_path(r'^posts/(?P<slug>[-\w]+)/$', views.post, name='post'),
    # here, - separated first and second potion as slug and pk. 
    # You may or may not choose to put - in slug value, it wont be a problem
    re_path(r'^blog/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', views.blog_post, name='blog_post'),
    # [\w.@+-] this means that any characters(., @, +, -) inside [] are supported as part of username
    re_path(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile'),
    # support exactly 4 occurences of digit ranging from 0 to 9
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive, name='year'),
    
    # to link to each board topics page for adding form to add new topic for that particular board 
    # by accessing the board primary key
    re_path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
]
