from django.urls import  path
from . import views

urlpatterns = [ # BURDA: url leri ve onların çağıracağı fonksiyonları yazıyoruz
    path("", views.index),
    path("index", views.index),
    path("blogs", views.blogs),
    path("blogs/<int:id>", views.blog_details),
]