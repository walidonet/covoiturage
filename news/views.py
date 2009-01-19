from django.shortcuts import render_to_response
from covoiturage.news.models import News

def news_view(request):
	# du plus recent au plus vieux, limite a 5, peut etre prevoir une configuration
	# a propos du nb max de news a garder, le reste dans les archives.
	news_list = News.objects.order_by('-pub_date')[:5]
	return render_to_response('base.html',{ 'news': news_list})
