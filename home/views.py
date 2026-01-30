from django.shortcuts import render
from django.views.generic.base import TemplateView
from products.models import product
from site_module.models import Slider,SiteSetting
# Create your views here.
from . import models

# def index(request):
#     return render(request,'home/home.html')

class index(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = product.objects.all()
        sliders = Slider.objects.filter(is_active=True)
        context = {
            'products':products,
            'sliders':sliders
        }
        return context

class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context
