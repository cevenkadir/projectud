from django.shortcuts import render
#from django.http import HttpResponse
from django.views.generic import TemplateView

import socket, urllib.request, json, requests

def check_server(url, port):
    r = requests.get("https://"+url)
    try:
        if r.json()['status']:
            return True
        else:
            return False
    except:
        return False



    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ock.settimeout(5)
    #result = sock.connect_ex((url, port))
    #if result == 0:
    #    return True
    #else:
    #    try:
    #        urllib.request.urlopen(url)
    #    except urllib.error.HTTPError as err:
    #        if err.code == 404:
    #            return False
    #        else:
    #            return True

class HomePageView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['raspi_status'] = check_server('projectud-kadrocuk.pitunnel.com', 80)
        return context