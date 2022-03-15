from django.contrib import admin
from .models import Blog, Category


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_home", "selected_categories")
    list_editable = ("is_active", "is_home")
    #list_filter = ("category",)

    def selected_categories(self, obj):
        html = ""

        for category in obj.categories.all():
            html+= category.name + " "
        return html

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
