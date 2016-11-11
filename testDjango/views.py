from django.shortcuts import render
import urllib
import httplib2
import http.client
from django.http import HttpResponse, Http404


def band_listing(request):
    """A view of all bands."""

    # return render(request, 'templates/test.html', {'bands': '1'})
    return HttpResponse("Hello NowaMagic!")