from covoiturage.news.models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
	model = News

admin.site.register(News ,NewsAdmin)