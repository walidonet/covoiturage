# -*- coding: utf-8 -*-
from covoiturage.news.models import News
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from news.models import NewsForm

def news_view(request):
    # du plus recent au plus vieux, limite a 5, peut etre prevoir une configuration
    # a propos du nb max de news a garder, le reste dans les archives.
    if request.user.is_authenticated():
        news_list = News.objects.order_by('-pub_date')[:3]
    else:
        news_list = News.objects.filter(is_public=True).order_by('-pub_date')[:3]
    return render_to_response('news/news.html',{'news': news_list}, RequestContext(request))

def list_all(request):
    if request.user.is_authenticated():
        news_list = News.objects.order_by('-pub_date')
    else:
        news_list = News.objects.filter(is_public=True).order_by('-pub_date')
    return render_to_response('news/archives.html',{'news_list': news_list}, RequestContext(request))

@user_passes_test(lambda u: u.has_perm('news.add_news'), login_url='/news/')
def add(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        news = form.save(commit=False)
        news.author = request.user
        news.save()
        request.user.message_set.create(message='L\'avis a bien été ajouté')
        return HttpResponseRedirect('/news/')
    else:    
        form = NewsForm()
    return render_to_response('news/add_news.html', {'form': form},RequestContext(request))

@user_passes_test(lambda u: u.has_perm('news.change_news'), login_url='/news/')
def edit(request, news_id):
    try:
        ref = request.META.get('HTTP_REFERER')
        n = News.objects.get(pk=news_id)
        if request.method == 'POST':
            form = NewsForm(request.POST, instance=n)
            if form.is_valid():
                form.save()
                request.user.message_set.create(message='L\'avis a bien été modifié')
            else:
                request.user.message_set.create(message='L\'avis n a pas été modifié')
            return HttpResponseRedirect('/news/')
        else:
            form = NewsForm(instance=n)
            return render_to_response('news/edit_news.html', {'form': form,'ref': ref},RequestContext(request))
    except News.DoesNotExist:
        request.user.message_set.create(message='L\'avis demandé n\'existe pas')
        return HttpResponseRedirect('/news/')

@user_passes_test(lambda u: u.has_perm('news.delete_news'), login_url='/news/')
def delete(request, news_id):
    try:
        n = News.objects.get(pk=news_id)
        n.delete()
        request.user.message_set.create(message="L\'avis a bien été supprimé")
        return HttpResponseRedirect('/news/')
    except News.DoesNotExist:
        request.user.message_set.create(message="Une erreur est survenue pendant la suppression de cet avis")
        return HttpResponseRedirect('/news/')  

def show(request, news_id):
    try:
        n = News.objects.get(pk=news_id)
        return render_to_response('news/show.html', {'news':n}, RequestContext(request))
    except News.DoesNotExist:
        request.user.message_set.create(message='L\'avis demandé n\'existe pas')
        return HttpResponseRedirect('/news/')