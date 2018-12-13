from django.contrib import admin

from .models import Article, Comment

admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","author","created_date","content"]
    list_display_links = ["title","created_date"]
    search_fields = ["title"]
    list_filter = ["created_date","title","author"]
    list_editable = ["author"]            #içeriği değiştirebildiğim komut
    class Meta:
        model = Article