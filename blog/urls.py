from django.urls import path
from . import views

urlpatterns = [  # BURDA: url leri ve onların çağıracağı fonksiyonları yazıyoruz
    path("", views.index, name="home"),
    path("index", views.index),
    path("blogs", views.blogs, name="blogs"),
    path("category/<slug:slug>", views.blogs_by_category, name="blogs_by_category"),
    path("blogs/<slug:slug>", views.blog_details, name="blog_details"),
]
