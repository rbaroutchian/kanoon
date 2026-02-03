from django.shortcuts import render,redirect
from django.views.generic.base import View
from . form import RegisterModelForm,LoginModelForm, EditProfileModelForm
from . models import user
from django.contrib.auth import authenticate, login,logout
from django.http import HttpRequest
from django.urls import reverse
from cinema.models import MovieReserve
from products.models import pish_sabt
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class RegisterAccount(View):
    def get(self, request):
        # form = RegisterModelForm()
        return render(request, 'account/register.html')


    def post(self, request):
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            if user.objects.filter(username=phone).exists():

                return render(request, 'account/register.html',
                              {'form': form,'error_message': 'این شماره قبلاً ثبت شده است در صورت عدم موفقیت برای ثبت نام با واحد پشتیبانی تماس بگیرید.'})
            u = form.save(commit=False)
            u.username = phone
            u.set_password(password)
            u.save()
            return redirect('home_page')

        return render(request, 'account/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginModelForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginModelForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                u = user.objects.get(username=username)
            except user.DoesNotExist:

                return render(request, 'account/login.html', {'form': form,
                                                              'error_message': 'عدم صحت اطلاعات ورودی'})

            auth_user = authenticate(
                request,
                username=u.username,  # چون username = mobile
                password=password
            )

            if auth_user:
                login(request, auth_user)
                next_url = request.POST.get('next') or request.GET.get('next')

                return redirect(next_url or 'profile_page')
                # return redirect('profile_page')
            else:
                form.add_error(None, 'شماره موبایل یا رمز عبور اشتباه است')

        return render(request, 'account/login.html', {'form': form})

class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = user.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        reserve = MovieReserve.objects.filter(user=request.user,is_confirmed=True).select_related('movie','show_time')
        context = {
            'form': edit_form,
            'current_user': current_user,
            'reserve':reserve
        }
        return render(request, 'account/profile.html', context)

    def post(self, request: HttpRequest):
        current_user = user.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)

        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'account/profile.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


class MyReservationsView(LoginRequiredMixin, View):
    def get(self, request):
        reserves = MovieReserve.objects.filter(
            user=request.user,is_confirmed=True
        ).select_related('movie', 'show_time')

        return render(request, 'account/include/reserv.html', {
            'reserves': reserves,
            'current_user': request.user

        })


class ClassPishView(LoginRequiredMixin, View):
    def get(self, request):
        pish = pish_sabt.objects.filter(
            user_pish=request.user
        )

        return render(request, 'account/include/pish.html', {
            'pish_sabtenam': pish,
            'current_user': request.user
        })