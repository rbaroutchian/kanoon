from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import ListView
from .models import movie, MovieReserve, ShowTime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import transaction
from account.models import user
from django.db.models import Sum






# Create your views here.
def movielist(request):
    return render(request,'cinema/movie_list.html')

class movieListView(ListView):
    template_name = 'cinema/movie_list.html'
    model = movie
    context_object_name = 'movies'

class MovieReserveView(LoginRequiredMixin, View):
    login_url = 'account/login/'

    def get(self, request, pk):
        select_movie = get_object_or_404(movie, pk=pk)
        return render(request, 'cinema/movie_reserve.html', {'movie': select_movie})

    def post(self, request, pk):
        select_movie = get_object_or_404(movie, pk=pk)

        try:
            count = int(request.POST.get('count'))
        except (TypeError, ValueError):
            return self._error(request, select_movie, 'تعداد بلیط نامعتبر است')

        if count < 1:
            return self._error(request, select_movie, 'تعداد بلیط باید حداقل ۱ باشد')

        max_buy = select_movie.max_ticket_per_user

        if count > max_buy:
            return self._error(
                request, select_movie,
                f'حداکثر تعداد مجاز برای هر خرید {max_buy} بلیط است'
            )

        with transaction.atomic():
            movie_locked = movie.objects.select_for_update().get(pk=pk)

            if count > movie_locked.capacity:
                return self._error(
                    request,
                    movie_locked,
                    'ظرفیت سالن برای این تعداد بلیط کافی نیست'
                )

            movie_locked.capacity -= count
            movie_locked.save(update_fields=['capacity'])

            reserve= MovieReserve.objects.create(
                user=request.user,
                movie=movie_locked,
                count=count,
                is_confirmed=False
            )

        return redirect('reserve_receipt', tracking_code=reserve.tracking_code)

    def _error(self, request, movie, message):
        return render(request, 'cinema/movie_reserve.html', {
            'movie': movie,
            'error': message
        })


class MovieReserveView2(LoginRequiredMixin, View):
    login_url = '/account/login/'

    def get_reserved_seats(self, show):
        """لیست شماره صندلی‌های رزرو شده برای یک سانس"""
        seats = []
        for r in show.reservations.all():
            if r.seats:
                seats += r.seats.split(',')
        return [int(s) for s in seats]

    def get(self, request, movie_id):
        movie_obj = get_object_or_404(movie, pk=movie_id)
        return render(request, 'cinema/r2.html', {
            'movie': movie_obj,
            'show_times': movie_obj.show_times.all(),
        })

    def post(self, request, movie_id):
        movie_obj = get_object_or_404(movie, pk=movie_id)
        show_time_id = request.POST.get('show_time')
        selected_show = get_object_or_404(ShowTime, pk=show_time_id)

        selected_seats = request.POST.get('selected_seats', '')

        # فقط انتخاب سانس (نه رزرو)
        if not selected_seats:
            return render(request, 'cinema/r2.html', {
                'movie': movie_obj,
                'show_times': movie_obj.show_times.all(),
                'selected_show': selected_show,
                'reserved_seats': self.get_reserved_seats(selected_show),
                'seat_layout': movie_obj.seat_layout(),
            })

        seat_list = [int(s) for s in selected_seats.split(',')]

        # محدودیت رزرو هر کاربر
        user_taken = MovieReserve.objects.filter(
            user=request.user,
            movie=movie_obj
        ).aggregate(total=Sum('count'))['total'] or 0

        remaining_for_user = movie_obj.remaining_per_user
        if len(seat_list) > remaining_for_user:
            return self.error(
                request, movie_obj, selected_show,
                f'شما فقط {remaining_for_user} صندلی دیگر می‌توانید انتخاب کنید'
            )

        # ثبت نهایی رزرو با تراکنش
        with transaction.atomic():
            locked_show = ShowTime.objects.select_for_update().get(pk=selected_show.pk)
            reserved = self.get_reserved_seats(locked_show)

            # بررسی صندلی‌های رزرو شده
            if any(s in reserved for s in seat_list):
                return self.error(
                    request, movie_obj, selected_show,
                    'یکی از صندلی‌ها قبلاً رزرو شده'
                )

            # ایجاد رزرو
            MovieReserve.objects.create(
                user=request.user,
                movie=movie_obj,
                show_time=locked_show,
                seats=','.join(map(str, seat_list)),
                count=len(seat_list),
                is_confirmed=True
            )

            # کم کردن ظرفیت کل و ظرفیت هر کاربر
            movie_obj.remaining_capacity -= len(seat_list)
            movie_obj.remaining_per_user -= len(seat_list)
            movie_obj.save()

        return render(request, 'cinema/r2.html', {
            'movie': movie_obj,
            'show_times': movie_obj.show_times.all(),
            'selected_show': selected_show,
            'reserved_seats': self.get_reserved_seats(selected_show),
            'seat_layout': movie_obj.seat_layout(),
            'success': f'رزرو با موفقیت انجام شد ({len(seat_list)} صندلی ثبت شد)'
        })

    def error(self, request, movie_obj, show, message):
        return render(request, 'cinema/r2.html', {
            'movie': movie_obj,
            'show_times': movie_obj.show_times.all(),
            'selected_show': show,
            'reserved_seats': self.get_reserved_seats(show) if show else [],
            'seat_layout': movie_obj.seat_layout(),
            'error': message
        })


class ReserveReceiptView(LoginRequiredMixin, View):
    def get(self, request, tracking_code):
        reserve = get_object_or_404(
            MovieReserve,
            tracking_code=tracking_code,
            user=request.user
        )

        return render(request, 'cinema/receipt.html', {
            'reserve': reserve
        })