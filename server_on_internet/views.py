from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView



import socket, urllib.request, json, requests

from .models import Muon
from .forms import UploadParticlesForm
from django.views.generic.edit import FormView

from collections import Counter

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


class UploadParticlesView(FormView):
    form_class = UploadParticlesForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '#success'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            print(files)
            for f in files:
                muon_i = Muon.objects.create(image=f)
                muon_i.process_muon()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class DataView(TemplateView):
    template_name = 'data.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DataView, self).get_context_data(*args, **kwargs)
        context['counted_angles'] = self.muons()
        return context

    def muons(self):
        all_muons = Muon.objects.all()
        all_angles = [muon_i.angle for muon_i in all_muons]

        counted_angles = dict(Counter(all_angles))
        counted_angles = dict(sorted(counted_angles.items()))
        return counted_angles