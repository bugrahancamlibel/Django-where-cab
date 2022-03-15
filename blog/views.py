from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog, Category



# Create your views here.

# BURDA: urls.py daki url lere karşılık gelecek fonksiyonları yazıyoruz.
def index(request):
    context = {
        "blogs": Blog.objects.filter(is_home=True, is_active=True),
        "categories": Category.objects.all()
    }
    return render(request, "blog/index.html", context)


def blogs(request):
    context = {
        "blogs": Blog.objects.filter(is_active=True),
        "categories": Category.objects.all()
    }
    return render(request, "blog/blogs.html", context)


def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    return render(request, "blog/blog-details.html", {
        "blog": blog
    })

def blogs_by_category(request, slug):
    pass