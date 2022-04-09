from django.shortcuts import render
from .models import Appointment
import time, datetime
from django.http import HttpResponse

DAYS = ['Poniedzialek', 'Wtorek', 'Sroda', 'Czwartek', 'Piatek', 'Sobota', 'Niedziela']

def home(request):
    if request.method == 'POST':
        name = request.POST.getlist('aktywnosc')[0]
        day = request.POST.getlist('dzien')[0]
        godzina = request.POST.getlist('godzina')
        minuty = request.POST.getlist('minuty')
        app_time = godzina[0] + ':' + minuty[0]
        app = Appointment(name=name, day=day, time=app_time)
        app.save()
    format = "%H:%M"
    #Appointment.objects.all().delete()
    appointments = Appointment.objects.all()
    appointments_sorted = sorted(appointments, key=lambda elem: time.strptime(elem.time, format))
    print(appointments_sorted)
    today = datetime.datetime.today()
    week_day = today.weekday()
    days_sorted = DAYS[week_day:] + DAYS[:week_day]
    appointments_sorted_final = []
    for day in days_sorted:
        for elem in appointments_sorted:
            if elem.day == day:
                appointments_sorted_final.append(elem)
    print(appointments_sorted_final)

    return render(request, 'hmi/home.html', {'wydarzenia': appointments_sorted_final[:5]})
# Create your views here.
