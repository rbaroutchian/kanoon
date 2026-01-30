from django.db import models
import uuid
import account.models


# Create your models here.
class movie(models.Model):
    title= models.CharField(max_length=300,blank=True,null=True,verbose_name='عنوان فیلم')
    day = models.CharField(max_length=300,blank=True,null=True,verbose_name='روز اکران')
    movie_time = models.CharField(max_length=300,blank=True,null=True,verbose_name='مدت زمان')
    start = models.TimeField(blank=True,null=True,verbose_name='ساعت شروع سانس')


    seats_left = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد صندلی سمت چپ')
    seats_right = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد صندلی سمت راست')


    capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name='ظرفیت')
    remaining_capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name='ظرفیت باقی‌مانده')

    max_ticket_per_user = models.PositiveIntegerField(default=4,verbose_name='حداکپر رزرو برای هر نفر')
    remaining_per_user = models.PositiveIntegerField(default=4, verbose_name='ظرفیت باقی‌مانده برای هر نفر')

    poster = models.ImageField(upload_to='',blank=True,null=True,verbose_name='پوستر فیلم')
    is_active= models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    short_desc = models.CharField(max_length=300,blank=True,null=True,verbose_name='توضیحات کوتاه')
    description= models.CharField(max_length=500, blank=True,null=True,verbose_name='توضیحات')
    slug = models.SlugField(default="", blank=True, db_index=True)

    def get_absolute_url(self):
        return reverse('#', args=[self.slug])

    def seat_layout(self):
        """ساختار افقی صندلی‌ها: راست سپس چپ، شماره‌ها پشت سر هم"""
        layout = []
        if not self.capacity or not self.seats_left or not self.seats_right:
            return layout

        total_per_row = self.seats_left + self.seats_right
        total_rows = (self.capacity // total_per_row) + (1 if self.capacity % total_per_row else 0)
        seat_number = 1

        for row in range(1, total_rows + 1):
            right = []
            left = []
            # سمت راست
            for _ in range(self.seats_right):
                if seat_number <= self.capacity:
                    right.append(seat_number)
                    seat_number += 1
            # سمت چپ
            for _ in range(self.seats_left):
                if seat_number <= self.capacity:
                    left.append(seat_number)
                    seat_number += 1
            layout.append({'row_number': row, 'right': right, 'left': left})
        return layout


    def seat_numbers(self):
        """لیست شماره صندلی‌ها"""
        return range(1, self.capacity + 1)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم ها'


class ShowTime(models.Model):
    movie = models.ForeignKey(movie, on_delete=models.CASCADE, related_name='show_times')
    time = models.DateTimeField(verbose_name='زمان سانس')
    capacity = models.PositiveIntegerField(default=50,blank=True,null=True)


    def __str__(self):
        return f"{self.movie.title} - {self.time}"

    class Meta:
        verbose_name = 'سانس'
        verbose_name_plural = 'سانس ها'



class MovieReserve(models.Model):
    user = models.ForeignKey(account.models.user, on_delete=models.CASCADE, verbose_name='کاربر')
    movie = models.ForeignKey(movie, on_delete=models.CASCADE, related_name='reservations', verbose_name='فیلم')
    show_time = models.ForeignKey(ShowTime,blank=True,null=True, on_delete=models.CASCADE, related_name='reservations')
    seats = models.CharField(max_length=200, blank=True,null=True, verbose_name='شماره صندلی‌ها')
    tracking_code = models.CharField(max_length=36,null=True,unique=True,editable=False,verbose_name='کد رهگیری')
    count = models.PositiveIntegerField(default=1, verbose_name='تعداد بلیط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ رزرو')
    is_confirmed = models.BooleanField(default=False, verbose_name='رزرو تایید شده')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = uuid.uuid4().hex.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'رزرو فیلم'
        verbose_name_plural = 'رزروها'
