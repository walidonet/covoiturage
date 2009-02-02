# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from covoiturage.news.models import News
from news.models import NewsForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.template import RequestContext

def news_view(request):
    # du plus recent au plus vieux, limite a 5, peut etre prevoir une configuration
    # a propos du nb max de news a garder, le reste dans les archives.
    if request.user.is_authenticated():
        news_list = News.objects.order_by('-pub_date')[:5]
    else:
        news_list = News.objects.filter(is_public=True).order_by('-pub_date')[:5]
    return render_to_response('news/news.html',{ 'news': news_list, 'user': request.user}, RequestContext(request))

@user_passes_test(lambda u: u.has_perm('news.add_news'), login_url='/news/')
def add(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        news = form.save(commit=False)
        news.author = request.user
        news.save()
        return HttpResponseRedirect('/news/')
    else:    
        form = NewsForm()
    return render_to_response('news/add_news.html', {'form': form},RequestContext(request))

@user_passes_test(lambda u: u.has_perm('news.change_news'), login_url='/news/')
def edit(request, news_id):
    #lance News.doesnotexist exception
    ref = request.META.get('HTTP_REFERER')
    n = News.objects.get(pk=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=n)
        if form.is_valid():
            form.save()
            message = 'L\'avis a bien été modifié'
        else:
            message = 'L\'avis n a pas été modifié'
        return render_to_response('news/edit_news.html', {'form': form,'message':message,})
    else:
        form = NewsForm(instance=n)
        return render_to_response('news/edit_news.html', {'form': form,'ref': ref})

@user_passes_test(lambda u: u.has_perm('news.delete_news'), login_url='/news/')
def delete(request, news_id):
    n = News.objects.get(pk=news_id)
    n.delete()
    return HttpResponseRedirect('/news/')
        