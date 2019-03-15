from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

import socket, urllib.request, json, requests

def check_server(url, port):
    if url == "localhost":
        http_type = "http://"
    else:
        http_type = "https://"
    try:
        r = requests.post("{}{}:{}".format(http_type, url, port), json={"auth_key": settings.AUTH_KEY})
        return r.json()['status']
    except:
        return False

class HomePageView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['raspi_status'] = check_server('localhost', 5000)
        #context['raspi_status'] = check_server('projectud-kadrocuk.pitunnel.com', 80)
        return context