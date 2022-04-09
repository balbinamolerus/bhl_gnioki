from django.shortcuts import render
from .models import Appointment
from django.http import HttpResponse

def home(request):
    if request.method == 'POST':

        name = request.POST.getlist('aktywnosc')
        day = request.POST.getlist('dzien')
        godzina = request.POST.getlist('godzina')
        minuty = request.POST.getlist('minuty')

        time = godzina[0] + ':' + minuty[0]
        app = Appointment(name=name, day=day, time=time)
        print(time)
        app.save()
    return render(request, 'hmi/home.html')
# Create your views here.
