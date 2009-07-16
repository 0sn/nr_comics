from django.views import generic
from django.views.decorators.vary import vary_on_cookie
from models import Comic
from nr_utils import render_with_request
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
import datetime
from django.shortcuts import get_object_or_404

def index(request):
    """the front page"""
    comic = Comic.comics.public().order_by('-date')[0]
        
    return render_with_request(
        "nr_comics/front.html",
        {"comic": comic},
        request
    )

def comic(request, slug):
    """the page of an individual comic"""
    comic = get_object_or_404(Comic, sequence=slug)
    return render_with_request(
        "nr_comics/comic_detail.html",
        {"comic": comic},
        request
    )

def archive(request):
    return generic.list_detail.object_list(
        request,
        queryset = Comic.comics.public(),
        template_object_name = "comic"
    )

def comic_image(request, slug):
    """the image for a particular comic"""
    c = get_object_or_404(Comic, sequence=int(slug))
    return HttpResponsePermanentRedirect(c.comic.url)
