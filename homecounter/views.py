from django.shortcuts import render, redirect
from .models import Counters, Languages, Cost
from .forms import CostFormEN, CostFormUA
from user.models import Bweller
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse, HttpResponse
from datetime import datetime, date, timedelta
from collections import defaultdict
from user.forms import BwellerRedactionFormEN, BwellerRedactionFormUA, BwellerRedactionFormUAAdmin, BwellerRedactionFormENAdmin
from django.core.paginator import Paginator
from django.db.models import Sum, Case, When, F, Q
from django.utils import timezone
from datetime import timedelta
import json
import hashlib
from random import randint
from tensorflow import keras
import numpy as np

def control_identifier(request):
    time_identifier = request.GET.get('time_identifier')
    ip_address = request.META.get('REMOTE_ADDR')
    try:
        user = Bweller.objects.get(time_identifier=time_identifier)
    except:
        return redirect(reverse_lazy('user:index'))
        
    time_identifier_control = hashlib.sha256(f'{user.login}2jk6lo{ip_address}{date.today()}'.encode()).hexdigest()
    if time_identifier is None or not time_identifier_control == user.time_identifier:
        return redirect(reverse_lazy('user:index'))
    return user

def get_language(user, leng='ua'):
    try:
        user.language
    except:
        user.language = leng
    leng = user.language
    queryset = Languages.objects.all()
    leng_dict = {}
    if leng == 'ua':
        for obj in queryset:
            leng_dict[obj.key] = obj.ua
    if leng == 'en':
        for obj in queryset:
            leng_dict[obj.key] = obj.en
    return leng_dict


class Profile_admin(View):
    def get(self, request, *args, **kwargs):
        user = control_identifier(request)
        
        counters_list = []
        for object_bweller in list(Bweller.objects.values_list('identifier', flat=True)):
            counters_data = list(Counters.objects.filter(identifier=object_bweller).values('power', 'datetime'))
       
            for record in counters_data:
                record['datetime'] = record['datetime'].isoformat()
        
            for i in range(len(counters_data) - 1, 0, -1):
                counters_data[i]['power'] = counters_data[i]['power'] - counters_data[i - 1]['power']
            counters_list.append(counters_data)

        hourly_power_sum = defaultdict(float)

        for sublist in counters_list:
            for item in sublist:
                datetime = item['datetime'][:13] 
                hourly_power_sum[datetime] += item['power']

        hourly_power = []
        for key, value in hourly_power_sum.items():
            hourly_power.append({'power': value, 'datetime': key + ':00:00+00:00'})

        return render(
            request,
            'profile_admin.html',
            {    
                'leng': get_language(user),
                'user': user,
                'counters_data': hourly_power
            }
        )


class Profile(View):
    def get(self, request, *args, **kwargs):
        user = control_identifier(request)
        try:
            counters_data = list(Counters.objects.filter(identifier=user.identifier).values('power', 'datetime'))
        except AttributeError:
            return redirect(reverse_lazy('user:index'))
        
        for record in counters_data:
            record['datetime'] = record['datetime'].isoformat()
        
        for i in range(len(counters_data) - 1, 0, -1):
            counters_data[i]['power'] = counters_data[i]['power'] - counters_data[i - 1]['power']

        
        return render(
            request,
            'profile.html',
            {    
                'cost': Cost.objects.first(),
                'leng': get_language(user),
                'user': user,
                'counters_data': counters_data
            }
        )
    

  
class Settings_user(View):
    def get(self, request, *args, **kwargs):
        user = control_identifier(request)
        if not user:
            return redirect(reverse_lazy('user:index'))

        try:
            counters_data = list(Counters.objects.filter(identifier=user.identifier).values('power', 'datetime'))
        except AttributeError:
            return redirect(reverse_lazy('user:index'))
        if user.language == 'ua':
            form = BwellerRedactionFormUA(instance=user)
        else:
            form = BwellerRedactionFormEN(instance=user)
        return render(request, 'settings_profile.html', {
            'form': form,
            'user': user,
            'leng': get_language(user)
        })

    def post(self, request, *args, **kwargs):
        user = control_identifier(request)
        if not user:
            return redirect(reverse_lazy('user:index'))
        if user.language == 'ua':
            form = BwellerRedactionFormUA(request.POST, request.FILES, instance=user)
        else:
            form = BwellerRedactionFormEN(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('/profile/profile_user/?time_identifier=' + str(user.time_identifier))  

        return render(request, 'settings_profile.html', {
            'leng': get_language(user),
            'form': form,
            'user': user
        })
    
class out(View):
    def get(self, request, *args, **kwargs):
        time_identifier = request.GET.get('time_identifier')
        user = Bweller.objects.get(time_identifier=time_identifier)
        user.time_identifier = None
        user.save()
        return redirect(reverse_lazy('user:index'))
    

class Settings_admin(View):
    def get(self, request, *args, **kwargs):
        user = control_identifier(request)
        try:
            counters_data = list(Counters.objects.filter(identifier=user.identifier).values('power', 'datetime'))
        except AttributeError:
            return redirect(reverse_lazy('user:index'))
        cost = Cost.objects.get(id=1)
        if user.language == 'ua':
            form = BwellerRedactionFormUAAdmin(instance=user)
            cost_form = CostFormUA(instance=cost)
        else:
            form = BwellerRedactionFormENAdmin(instance=user)
            cost_form = CostFormEN(instance=cost)
                
        return render(request, 'settings_admin.html', {
            'form': form,
            'cost_form': cost_form,
            'user': user,
            'leng': get_language(user)
        })

    def post(self, request, *args, **kwargs):
        user = control_identifier(request)
        if not user:
            return redirect(reverse_lazy('user:index'))
        
        if user.language == 'ua':
            form = BwellerRedactionFormUAAdmin(request.POST, request.FILES, instance=user)
            cost_form = CostFormUA(request.POST)
        else:
            form = BwellerRedactionFormENAdmin(request.POST, request.FILES, instance=user)
            cost_form = CostFormEN(request.POST)

        if form.is_valid() and cost_form.is_valid():
            form.save()
            cost_form.save()
            return redirect('/profile/profile_admin/?time_identifier=' + str(user.time_identifier))

        return render(request, 'settings_admin.html', {
            'leng': get_language(user),
            'form': form,
            'cost_form': cost_form,
            'user': user
        })
    
  

class Summari_home(View):
    def get(self, request, *args, **kwargs):
        user = control_identifier(request)
        try:
            today = timezone.now().date()
            first_day_current_month = today.replace(day=1)
            last_month = first_day_current_month - timedelta(days=1)
            first_day_last_month = last_month.replace(day=1)

            this_month_start = timezone.make_aware(timezone.datetime.combine(first_day_current_month, timezone.datetime.min.time()))
            last_month_start = timezone.make_aware(timezone.datetime.combine(first_day_last_month, timezone.datetime.min.time()))
            next_month_start = timezone.make_aware(timezone.datetime.combine((first_day_current_month + timedelta(days=31)).replace(day=1), timezone.datetime.min.time()))
            apartment_query = request.GET.get('apartment_number')

            

            if apartment_query:
                residents = Bweller.objects.filter(apartment_number__apartment_number=apartment_query, is_admin=False).select_related('apartment_number')
            else:
                residents = Bweller.objects.filter(is_admin=False).select_related('apartment_number')


            data = []

            for resident in residents:
                counters_data = Counters.objects.filter(
                    identifier=resident.identifier,
                    datetime__gte=last_month_start,
                    datetime__lt=next_month_start
                ).order_by('datetime')

                counters_data = list(counters_data.values('power', 'datetime'))

                for i in range(len(counters_data) - 1, 0, -1):
                    counters_data[i]['power'] -= counters_data[i - 1]['power']

                def calculate_power(counters):
                    day_power = 0
                    night_power = 0
                    for counter in counters:
                        hour = counter['datetime'].hour
                        if 7 <= hour < 23:
                            day_power += counter['power']
                        else:
                            night_power += counter['power']
                    return day_power, night_power

                current_month_counters = [c for c in counters_data if this_month_start <= c['datetime'] < next_month_start]
                last_month_counters = [c for c in counters_data if last_month_start <= c['datetime'] < this_month_start]

                current_day_power, current_night_power = calculate_power(current_month_counters[1:])
                last_day_power, last_night_power = calculate_power(last_month_counters[1:])

                data.append({
                    'apartment_number': resident.apartment_number.apartment_number,
                    'first_name': resident.first_name,
                    'last_name': resident.last_name,
                    'current_day_power': current_day_power,
                    'current_night_power': current_night_power,
                    'last_day_power': last_day_power,
                    'last_night_power': last_night_power,
                })

        except AttributeError:
            return redirect(reverse_lazy('user:index'))

        paginator = Paginator(data, 2)  # Показывать 10 квартир на странице
        page_number = request.GET.get('page')
        leng = request.GET.get('leng')
        page_obj = paginator.get_page(page_number)

        return render(request, 'summari_home.html', {
            'leng': get_language(user, leng),
            'user': user,
            'page_obj': page_obj,
            'apartment_number': apartment_query,
        })

class Analize(View):
    def post (self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            x_trein = []
            for a in data:
                x_trein.append(float(a)/1000)
            
            x_trein = np.array([data])
            dict = {'value': keras.models.load_model('models/nero').predict(x_trein)[0][0].tolist()}
            return JsonResponse(dict, status=200)
        except json.JSONDecodeError:
            return JsonResponse(status=400)



def get_data(request):
    start_date = timezone.make_aware(datetime(2023, 5, 1, 0, 0, 0))
    end_date = timezone.make_aware(datetime(2024, 5, 10, 23, 0, 0))

    current_date = start_date
    random_value = 0
    while current_date <= end_date:
        random_value += randint(0, 2)
        counter = Counters(identifier="d5e36897929d71d0f29f554e0a7e6b8dc1b32b8f8dfb348686da7c26a37cdfec", power=random_value, datetime=current_date)
        counter.save()
        current_date += timedelta(hours=1)
    return JsonResponse(status=200)



       