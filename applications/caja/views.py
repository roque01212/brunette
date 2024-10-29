from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from.forms import CajaForm, CajaUpdateForm
from .models import Caja
# Create your views here.


class AperturaCaja(FormView):

    form_class = CajaForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/apertura_caja.html'


    def form_valid(self, form):
        user = self.request.user
        monto_inicial = form.cleaned_data['monto_inicial_caja']
        Caja.objects.crear_apertura_caja(user, monto_inicial)
        return super().form_valid(form)
    

    
class CierreCaja(FormView):
    form_class = CajaUpdateForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/cierre_caja.html'


    def form_valid(self, form):
        user = self.request.user
        total_ingresos = form.cleaned_data['total_ingresos']
        total_egresos = form.cleaned_data['total_egresos']
        Caja.objects.cerrar_caja(user, total_ingresos, total_egresos)
        return super().form_valid(form)
