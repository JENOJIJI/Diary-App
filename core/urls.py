from unicodedata import name
from django.urls import URLPattern, path

from .views import index, blog, detailedView, user_login, search, register, comment

app_name = 'core'
urlpatterns = [
    path('', index),
    path('blog/', blog, name='blog'),
    path('blog/<str:slug>', detailedView, name='detailed-blog'),
    path('search/', search, name='search'),
    path('login/', user_login, name='login'),
    path('sign-up/', register, name='signup'),
    path('comment/', comment, name='comment')
]