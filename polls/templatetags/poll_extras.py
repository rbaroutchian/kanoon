from django import template
import jdatetime


register = template.Library()


@register.filter(name='show_jalali_date')
def show_jalali_date(value, format='%Y/%m/%d'):
    if not value:
        return ""
    try:
        if hasattr(value, 'date'):
            jalali_date = jdatetime.date.fromgregorian(date=value.date())
        else:
            jalali_date = jdatetime.date.fromgregorian(date=value)

        return jalali_date.strftime(format)
    except Exception as e:
        return str(value)