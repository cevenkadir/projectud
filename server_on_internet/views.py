from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView


import socket
import urllib.request
import json
import requests

from .models import Muon
from .forms import UploadParticlesForm
from django.views.generic.edit import FormView

from collections import Counter

import numpy as np

from scipy.optimize import curve_fit


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
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
        context['counted_angles'] = muons()
        context['theortical_data'] = theortical_data()
        context['theortical_data_classical'] = theortical_data(
            includeTimeDilation=False)
        context['best_fitting'] = self.best_fitting()
        return context

    def best_fitting(self):
        all_muons = muons()
        x = np.array(list(all_muons.keys()))
        y = np.array(list(all_muons.values()))
        z = np.polyfit(x, y, 3)
        p = np.poly1d(z)

        num = 100
        angles = np.array(np.linspace(0, 90, num=num))

        # def func(x, a, b, c):
        #     return a * np.exp(-b * x) + c

        # popt, pcov = curve_fit(func, x, y)

        # y = func(x, *popt)

        # new_y = [y(angle_i) for angle_i in angles]
        new_y = [p(angle_i) for angle_i in angles]

        return dict(zip(angles, new_y))

# class MuonListView(TemplateView):
#     template_name = 'muon_list
# .html'

#     def get_context_data(self, *args, **kwargs):
#         context = super(MuonListView, self).get_context_data(*args, **kwargs)
#         context['muons'] = Muon.objects.all()
#         return context


class MuonListView(ListView):
    model = Muon
    template_name = 'muon_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'muons'  # Default: object_list
    paginate_by = 10
    queryset = Muon.objects.all()  # Default: Model.objects.all()


def handler404(request, exception):
    return render(request, 'error.html', status=404)


def handler500(request):
    return render(request, 'error.html', status=500)


def muons():
    all_muons = Muon.objects.all()
    all_angles = [muon_i.angle for muon_i in all_muons]

    counted_angles = dict(Counter(all_angles))
    counted_angles = dict(sorted(counted_angles.items()))
    return counted_angles

def theortical_data(includeTimeDilation=True):
        num = 100
        angles = np.array(np.linspace(0, 90, num=num))

        n = 1000

        num_muons_detected = Muon.objects.count()

        flux_dict = {}

        if includeTimeDilation:
            r_range_with_dilation = np.array(np.linspace(0.1, 0.7, num=n))

            flux_mean = np.zeros(num)

            for r_i in r_range_with_dilation:
                flux_i = np.power(
                    r_i, (1/np.cos(np.deg2rad(angles)) - 1)) * np.cos(np.deg2rad(angles))
                # print(flux_i)
                flux_mean += flux_i
                #flux_mean = np.add(flux_mean, flux_i)
            flux_mean = flux_mean / n
        else:
            r_no_time_dilation = 1.14e-10
            flux_mean = np.power(
                r_no_time_dilation, (1/np.cos(np.deg2rad(angles)) - 1)) * np.cos(np.deg2rad(angles))

        for i in range(num):
            flux_dict[angles[i]] = flux_mean[i] * muons()[0]
        return flux_dict

def calcError(request):
    measurement_data = muons()
    theo_data = theortical_data()

    error_list = []

    for key_i in measurement_data:

        value_i = measurement_data[key_i]
        value = theo_data[min(
            theo_data.keys(), key=lambda k: abs(k-key_i))]

        error_i = 100 * (value - value_i)/value
        error_list.append(error_i)

    return {'calcError': sum(error_list)/len(error_list)}
