from django.http import HttpResponse
from django.shortcuts import render

data = {
    "blogs": [
        {
            "id": 1,
            "title": "komple web dev",
            "image": "1.jpg",
            "is_active": True,
            "is_home": False,
            "description": "perfect course"
        },
        {
            "id": 2,
            "title": "python",
            "image": "1.jpg",
            "is_active": True,
            "is_home": True,
            "description": "perfect course"
        },
        {
            "id": 3,
            "title": "django kursu",
            "image": "1.jpg",
            "is_active": False,
            "is_home": True,
            "description": "perfect course"
        },
    ]
}


# Create your views here.

# BURDA: urls.py daki url lere karşılık gelecek fonksiyonları yazıyoruz.
def index(request):
    context = {
        "blogs": data["blogs"]
    }
    return render(request, "blog/index.html", context)


def blogs(request):
    context = {
        "blogs": data["blogs"]
    }
    return render(request, "blog/blogs.html", context)


def blog_details(request, id):
    # blogs = data["blogs"]
    # selectedBlog = None
    # for blog in blogs:
    #     if blog["id"] == id:
    #         selectedBlog = blog
    blogs = data["blogs"]
    selectedBlog = [blog for blog in blogs if blog["id"]==id][0]
    return render(request, "blog/blog-details.html", {
        "blog": selectedBlog
    })
