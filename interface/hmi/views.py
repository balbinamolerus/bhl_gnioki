from django.shortcuts import render
from .models import Appointment
import time, datetime
import random
from django.contrib import messages
from django.http import HttpResponse

DAYS = ['Poniedzialek', 'Wtorek', 'Sroda', 'Czwartek', 'Piatek', 'Sobota', 'Niedziela']
POCZATEK = ['Gdyby kózka nie skakała ', 'Gdzie kucharek sześć ', 'Bez pracy ', 'Gdzie kucharek sześć ',
            'Nie chwal dnia ', 'Dzieci i ryby ', 'Lepszy wróbel w garści ', 'Co ma wisieć ']
KONIEC = ['to by nóżki nie złamała.', 'tam nie ma co jeść.', 'nie ma kołaczy', 'tam nie ma co jeść.',
          'przed zachodem słońca.', 'głosu nie mają.', 'niż gołąb na dachu.', 'nie utonie.']

poczatek_dict = {key: value for value, key in enumerate(POCZATEK)}
koniec_dict = {key: value for value, key in enumerate(KONIEC)}

def home(request):
    if request.method == 'POST':
        name = request.POST.getlist('aktywnosc')[0]
        day = request.POST.getlist('dzien')[0]
        godzina = request.POST.getlist('godzina')
        minuty = request.POST.getlist('minuty')
        app_time = godzina[0] + ':' + minuty[0]
        app = Appointment(name=name, day=day, time=app_time)
        with open('/home/pi/bhl/bhl_gnioki/alerts.txt', 'a') as f:
            f.write(name + ';' + str(godzina[0]) + ':' + str(minuty[0]) + '\n')
        app.save()

    format = "%H:%M"
    #Appointment.objects.all().delete()
    appointments = Appointment.objects.all()
    appointments_sorted = sorted(appointments, key=lambda elem: time.strptime(elem.time, format))
    today = datetime.datetime.today()
    week_day = today.weekday()
    days_sorted = DAYS[week_day:] + DAYS[:week_day]
    appointments_sorted_final = []
    for day in days_sorted:
        for elem in appointments_sorted:
            if elem.day == day:
                appointments_sorted_final.append(elem)

    return render(request, 'hmi/home.html', {'wydarzenia': appointments_sorted_final[:5]})

poczatek_list=[]
def gra(request):
    random_pocz = random.choice(list(poczatek_dict.keys()))
    if request.method == 'POST':
        dokonczenie_idx = request.POST.getlist('przyslowie')[0]
        poczatek_list.append(poczatek_dict[random_pocz])
        if len(poczatek_list) == 1:
            return render(request, 'hmi/gra.html',
                          {'poczatek': random_pocz, 'dokonczenia': koniec_dict, 'poprawna': poczatek_dict[random_pocz]})
        print(poczatek_list[-2], dokonczenie_idx)
        if (int(dokonczenie_idx) == int(poczatek_list[-2])):
            messages.success(request, f'Udało się! Poprawnie dokończono przysłowie!')
        else:
            messages.warning(request, f'Niepoprawna odpowiedź :(. Spróbuj ponownie.')

    return render(request, 'hmi/gra.html', {'poczatek': random_pocz, 'dokonczenia':koniec_dict, 'poprawna': poczatek_dict[random_pocz]})
