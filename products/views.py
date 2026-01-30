from itertools import product

from django.shortcuts import render,redirect

from .form import pishSabtForm
from . models import product,pish_sabt
from django.views.generic import ListView,View,DetailView
# Create your views here.


def productlist(request):
    return render(request,'products/product_list.html')

class productListView(ListView):
    template_name = 'products/product_list.html'
    model = product
    context_object_name = 'products'

class pish_sabtenam(View):
    def get(self, request):
        product_id = request.GET.get('product_id')
        try:
            selected_product = product.objects.get(id=product_id)
        except (product.DoesNotExist, TypeError, ValueError):
            selected_product = None
        form = pishSabtForm()
        return render(request, 'products/pish_sabt.html', {
            'form': form,
            'products': product.objects.all(),
            'age_choices': pish_sabt.age_choice,
            'selected_product': selected_product

        })

    def post(self, request):
        form = pishSabtForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "پیش‌ثبت‌نام با موفقیت انجام شد"
            form = pishSabtForm()  # برای پاک کردن فرم بعد از submit
        else:
            success_message = None

        selected_product = None
        if 'product_choice' in request.POST:
            try:
                selected_product = product.objects.get(id=request.POST['product_choice'])
            except:
                pass

        return render(request, 'products/pish_sabt.html', {
            'form': form,
            'products': product.objects.all(),
            'age_choices': pish_sabt.age_choice,
            'selected_product': selected_product,
            'success_message': success_message
        })

class productDetailView(DetailView):
    template_name = 'products/product_detail.html'
    model = product
    context_object_name = 'productd'


