from django.db.models import Q, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import make_aware
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic.edit import FormView

from django.views.generic import DeleteView, UpdateView, ListView, TemplateView


from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt #
from io import BytesIO
import os
import base64
import tempfile
from reportlab.lib.pagesizes import letter #
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime, timedelta
from.forms import CajaForm, CajaUpdateForm
from .models import Caja, Mesas
from applications.cocina.models import Pedidos, DetallePedido, Productos

from applications.users.mixins import CajaPermisoMixin, AdminPermisoMixin
from .forms import PedidoForm, DetallePedidoForm, DetallePedidoUpdateForm

# Create your views here.


class AperturaCaja(CajaPermisoMixin, FormView):

    form_class = CajaForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/apertura_caja.html'


    def form_valid(self, form):
        user = self.request.user
        monto_inicial = form.cleaned_data['monto_inicial_caja']
        Caja.objects.crear_apertura_caja(user, monto_inicial)
        return super().form_valid(form)


class CierreCaja(CajaPermisoMixin, FormView):

    form_class = CajaUpdateForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/cierre_caja.html'
    login_url = reverse_lazy('users_app:User-Login')

    def form_valid(self, form):
        user = self.request.user
        total_ingresos = form.cleaned_data['total_ingresos']
        total_egresos = form.cleaned_data['total_egresos']
        
        # Verificar si existen pedidos pendientes o sin cobrar
        pedidos_pendientes = Pedidos.objects.filter(Q(pagado_pedido=False) | Q(pedido_listo=False))
        if pedidos_pendientes.exists():
            # Si existen pedidos pendientes, mostrar un mensaje de advertencia
            return self.render_to_response(self.get_context_data(
                form=form, mensaje_alerta="No se puede cerrar la caja. Existen pedidos pendientes o sin cobrar."
            ))

        # Liberar todas las mesas (actualizando 'disponible' a True)
        Mesas.objects.filter(mesa_dispnible=False).update(mesa_dispnible=True)
        # Si no hay pedidos pendientes, realizar el cierre de caja
        Caja.objects.cerrar_caja(user, total_ingresos, total_egresos)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasar el mensaje de alerta, si existe
        mensaje_alerta = kwargs.get('mensaje_alerta', '')
        context['mensaje_alerta'] = mensaje_alerta
        return context

    def get_ventas_info(self):
        """Obtenemos los detalles de los pedidos realizados antes de cerrar la caja"""
        ventas = Pedidos.objects.filter(caja__estado='abierta')  # Filtramos solo los pedidos realizados en cajas abiertas
        detalles_ventas = []

        for venta in ventas:
            detalles = DetallePedido.objects.filter(pedido=venta)
            total_venta = sum(d.subtotal for d in detalles)  # Calculamos el total de la venta
            detalles_ventas.append({
                'venta': venta,
                'detalles': detalles,
                'total_venta': total_venta
            })
        return detalles_ventas


def ventas_realizadas(request):
    # Obtener las ventas realizadas (caja abierta)
    ventas = Pedidos.objects.filter(caja__abierta_caja=True)  # Filtrar solo los pedidos con caja abierta

    # Obtener la fecha actual para el reporte
    fecha_actual = timezone.now().strftime("%d/%m/%Y")

    # Crear la respuesta HTTP para el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ventas_realizadas_{fecha_actual}.pdf"'

    # Crear el canvas para el PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('Ventas Realizadas')

    # Configurar márgenes
    margen_izquierda = 50
    margen_superior = 750
    margen_inferior = 50
    espacio_entre_filas = 15
    y_position = margen_superior  # Posición inicial para el contenido

    # Agregar título y fecha al encabezado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, y_position, "Ventas Realizadas - Detalles del Día")
    pdf.setFont("Helvetica", 12)
    y_position -= 20
    pdf.drawString(200, y_position, f"Fecha: {fecha_actual}")
    y_position -= 30  # Ajustamos para que haya un poco de espacio después del encabezado

    mesas = set(venta.mesa for venta in ventas)  # Obtener las mesas únicas

    for mesa in mesas:
        # Filtrar los pedidos por mesa
        pedidos_mesa = ventas.filter(mesa=mesa)

        # Agregar el nombre de la mesa
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margen_izquierda, y_position, f"Mesa {mesa.num_mesa}")
        y_position -= 20  # Espacio debajo del título de mesa

        # Encabezados de la tabla
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(margen_izquierda, y_position, "Producto")
        pdf.drawString(200, y_position, "Cantidad")
        pdf.drawString(300, y_position, "Subtotal")
        y_position -= espacio_entre_filas  # Espacio entre encabezado y filas

        # Recorrer los pedidos de la mesa y agregar los detalles
        for venta in pedidos_mesa:
            detalles = DetallePedido.objects.filter(pedido=venta)
            for detalle in detalles:
                pdf.setFont("Helvetica", 10)
                pdf.drawString(margen_izquierda, y_position, detalle.producto.nombre_prod)  # Nombre del producto
                pdf.drawString(200, y_position, str(detalle.total_pedido))  # Cantidad
                pdf.drawString(300, y_position, f"${detalle.subtotal:.2f}")  # Subtotal
                y_position -= espacio_entre_filas  # Espacio entre productos

                # Comprobar si hay espacio suficiente para la siguiente fila
                if y_position < margen_inferior:
                    pdf.showPage()  # Añadir una nueva página
                    y_position = margen_superior  # Restablecer la posición de la página

        # Calcular el total de la venta para la mesa
        total_venta_mesa = sum(d.subtotal for venta in pedidos_mesa for d in DetallePedido.objects.filter(pedido=venta))

        # Agregar el total de la venta de la mesa
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margen_izquierda, y_position, f"Total Venta Mesa {mesa.num_mesa}:")
        pdf.drawString(300, y_position, f"${total_venta_mesa:.2f}")
        y_position -= 30  # Espacio entre mesas

        # Comprobar si hay espacio suficiente para la siguiente mesa
        if y_position < margen_inferior:
            pdf.showPage()  # Añadir una nueva página
            y_position = margen_superior  # Restablecer la posición de la página

    pdf.save()
    return response


class CrearPedidoView(CajaPermisoMixin, FormView):
    template_name = 'caja/generar_pedido.html'
    form_class = PedidoForm
    success_url = reverse_lazy('caja_app:Crear_Pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formPedido'] = DetallePedidoForm()

        context['lista_pedidos'] = DetallePedido.objects.filter(
            pedido__pedido_listo=False
        ).order_by("-id")[:4]
        context['form_update'] = DetallePedidoUpdateForm()
        return context

    def form_valid(self, form):
        # Obtener y guardar los datos del pedido principal
        mesa = form.cleaned_data['mesa']
        tipo_pago = form.cleaned_data['tipo_pago_pedido']
        pagado = form.cleaned_data['pagado_pedido']

        # Guardar el detalle del pedido
        producto_id = self.request.POST.get('producto')
        producto = get_object_or_404(Productos, id=producto_id)
        total_pedido = int(self.request.POST.get('total_pedido'))

        # Verificar si hay suficiente stock
        if producto.stock_actual_prod < total_pedido:
            return JsonResponse({
                'success': False,
                'message': f"No hay suficiente stock de {producto.nombre_prod}. Stock disponible: {producto.stock_actual_prod}."
            })
        caja = get_object_or_404(Caja, abierta_caja=True)
        pedido = Pedidos.objects.crear_pedidos(caja, mesa, tipo_pago, pagado)
        Mesas.objects.update_mesa(mesa.id)


        # Crear el detalle del pedido
        DetallePedido.objects.crear_detalleP(pedido, producto, total_pedido)

        # Actualizar el stock del producto
        producto.stock_actual_prod -= total_pedido
        producto.save()

        # Devolver respuesta JSON de éxito
        return JsonResponse({
            'success': True,
            'message': f"Pedido creado correctamente. Stock actualizado para {producto.nombre_prod}."
        })



def filtrar_productos(request):
    query = request.GET.get('kword'," ").strip() # Término de búsqueda
    if query:  # Si hay un término de búsqueda
        productos = Productos.objects.filter(nombre_prod__icontains=query)
    else:  # Si el término está vacío
        productos = Productos.objects.none() 
    data = [{'id': prod.id, 'nombre': prod.nombre_prod} for prod in productos]
    return JsonResponse({'productos': data})


class DetallePedidoDeleteView(CajaPermisoMixin, DeleteView):
    model = Pedidos

    success_url = reverse_lazy('caja_app:Crear_Pedido')




class DetallePedidoUpdateView(CajaPermisoMixin, UpdateView):
    model = DetallePedido
    form_class = DetallePedidoUpdateForm
    template_name = 'caja/update.html'
    success_url = reverse_lazy('caja_app:Crear_Pedido')

    def form_valid(self, form):
        detalle = form.save(commit=False)

        # Recuperar la cantidad original antes de la actualización
        cantidad_original = DetallePedido.objects.get(pk=detalle.pk).total_pedido

        # Actualizar el stock del producto
        producto = detalle.producto
        producto.stock_actual_prod += cantidad_original  # Revertir la cantidad original
        producto.stock_actual_prod -= detalle.total_pedido  # Aplicar la nueva cantidad
        producto.save()

        # Actualizar el subtotal del pedido
        detalle.subtotal = detalle.total_pedido * producto.precio_prod
        detalle.save()

        # Si la solicitud es AJAX, devolver respuesta JSON
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True}, status=200)

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Usa get_object_or_404 para evitar un error si el objeto no existe
        self.object = get_object_or_404(DetallePedido, pk=kwargs['pk'])
        context = self.get_context_data()

        # Verificar si la solicitud es AJAX usando el encabezado
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"html": html}, status=200)

        # Si no es una solicitud AJAX, procesa normalmente
        return super().get(request, *args, **kwargs)


class PedidosListView(CajaPermisoMixin,ListView):
    model = DetallePedido
    template_name = "caja/pedidos.html"
    context_object_name='lista_pedidos'
    paginate_by= 9

    def get_queryset(self):
        # Mostrar todos los detalles de pedidos que no estén listos (categorías 0 y 1)
        return DetallePedido.objects.filter(
            pedido__pedido_listo=False,
            
        ).order_by('id')


class MarcarPedidoListoView(CajaPermisoMixin,View):
    def post(self, request, pk, *args, **kwargs):
        pedido = get_object_or_404(Pedidos, id=pk)
        if not pedido.pedido_listo:  # Verifica que no esté marcado aún
            pedido.pedido_listo = True
            pedido.save()
        return redirect('caja_app:Lista_Pedidos')


class MesasListView(CajaPermisoMixin,ListView):
    model = Mesas
    template_name = 'caja/lista_mesas.html'
    context_object_name = 'mesas'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mesas_con_pedidos_pendientes = Mesas.objects.filter(
            pedido_mesa__pagado_pedido=False
        ).distinct()
        context['cobrar'] = mesas_con_pedidos_pendientes
        return context

    
class MesasUpdateView(CajaPermisoMixin,UpdateView):
    model = Mesas
    fields = []  # Dejamos vacío porque no queremos mostrar un formulario completo
    success_url = reverse_lazy('caja_app:Lista_mesas')
    

    def post(self, request, *args, **kwargs):
        # Obtiene la mesa que se quiere actualizar
        mesa = get_object_or_404(Mesas, pk=kwargs['pk'])


        pedidos_pendientes = mesa.pedido_mesa.filter(
            Q(pagado_pedido=False) | Q(pedido_listo=False)
        )  # Asumiendo que hay un `related_name` 'pedido_mesa'

        if pedidos_pendientes.exists():
            return JsonResponse({'error': True, 'message': f'La mesa {mesa.num_mesa} tiene pedidos pendientes o aun no se no se pago'}, status=400)

        mesa.mesa_dispnible = True
        mesa.save()
        return JsonResponse({'success': True, 'message': f'La mesa {mesa.num_mesa} ha sido liberada correctamente.'})

    
class CobrarPedidosView(CajaPermisoMixin,View):

    def post(self, request, pk, *args, **kwargs):
        # Obtén la mesa que se desea cobrar
        mesa = get_object_or_404(Mesas, pk=pk)

        # Verifica si hay pedidos pendientes de pago para esta mesa
        pedidos_pendientes = mesa.pedido_mesa.filter(pagado_pedido=False)

        if pedidos_pendientes.exists():
            # Marcar todos los pedidos como pagados
            pedidos_pendientes.update(pagado_pedido=True)
            mesa.save()
        return redirect(reverse_lazy('caja_app:Lista_mesas'))
        

class GenerarPDFView(CajaPermisoMixin, View):
    def get(self, request, pk, *args, **kwargs):        
       # Obtener la mesa
        mesa = Mesas.objects.get(pk=pk)
        
        # Obtener todos los pedidos pendientes de la mesa
        pedidos = mesa.pedido_mesa.filter(pagado_pedido=False)
        
        if not pedidos:
            return HttpResponse("No se encontraron pedidos pendientes para esta mesa.", status=404)

        # Crear la respuesta con un encabezado de PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="pedidos_mesa_{mesa.num_mesa}.pdf"'

        # Crear el canvas para el PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle(f"Factura Mesa {mesa.num_mesa}")

        # Estilo del PDF
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 750, "Restaurante BRUNETTE")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(400, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Agregar el número de mesa
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(30, 700, f"Mesa: {mesa.num_mesa}")

        # Preparar datos para la tabla
        data = [["Producto", "Precio", "Cantidad", "Subtotal"]]  # Encabezado de la tabla
        total = 0
        
        # Recorrer todos los pedidos pendientes y agregar sus detalles a la tabla
        for pedido in pedidos:
            detalles = DetallePedido.objects.filter(pedido=pedido)
            
            for detalle in detalles:
                subtotal = detalle.total_pedido * detalle.producto.precio_prod
                total += subtotal
                data.append([
                    detalle.producto.nombre_prod,
                    f"${detalle.producto.precio_prod:.2f}",
                    detalle.total_pedido,
                    f"${subtotal:.2f}",
                ])

        # Agregar fila del total
        data.append(["", "", "Total:", f"${total:.2f}"])

        # Estilo de la tabla
        table = Table(data, colWidths=[200, 100, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4CAF50")),  # Fondo verde
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto blanco en encabezado
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrado
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado en encabezado
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor("#f9f9f9")),  # Fondo alternado
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes de la tabla
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#333333")),  # Texto negro
            ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),  # Fuente del total
        ]))

        # Ubicación de la tabla
        table.wrapOn(pdf, 50, 500)
        table.drawOn(pdf, 50, 450)

        # Mensaje de despedida
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 400, "¡Gracias por su visita! Esperamos verlo pronto.")

        # Cerrar el PDF
        pdf.showPage()
        pdf.save()

        return response
    

class RankingTortaView(AdminPermisoMixin, TemplateView):
    template_name = 'caja/ranking_menus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fecha límite del último mes
        fecha_limite = make_aware(datetime.now() - timedelta(days=30))
        # fecha_limite = datetime.now() - timedelta(days=30)
        
        # Consulta: Agrupar por producto y sumar cantidades
        ranking = (
            DetallePedido.objects.filter(pedido__fecha_hs_pedido__gte=fecha_limite)
            .values('producto__nombre_prod')  # Seleccionar el nombre del producto
            .annotate(cantidad_total=Sum('total_pedido'))  # Sumar la cantidad total pedida
            .order_by('-cantidad_total')[:5]  # Ordenar por cantidad y tomar los 5 primeros
        )

        # Preparar datos para el gráfico
        productos = [item['producto__nombre_prod'] for item in ranking]
        cantidades = [item['cantidad_total'] for item in ranking]

        # Generar el gráfico de torta
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            cantidades,
            labels=productos,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Paired.colors,
        )
        ax.set_title('Distribución de los 5 Pedidos Más Solicitados (Último Mes)', fontsize=12)

        # Convertir el gráfico a base64 para renderizarlo en la plantilla
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')

        # Pasar los datos al contexto
        context['grafico'] = graphic
        context['titulo'] = '5 Pedidos Más Solicitados (Último Mes)'
        return context


def ranking_torta_pdf(request):

    
    # Fecha límite del último mes (con zona horaria)
    fecha_limite = make_aware(datetime.now() - timedelta(days=30))
    
    # Consulta: Agrupar por producto y sumar cantidades
    ranking = (
        DetallePedido.objects.filter(pedido__fecha_hs_pedido__gte=fecha_limite)
        .values('producto__nombre_prod')  # Seleccionar el nombre del producto
        .annotate(cantidad_total=Sum('total_pedido'))  # Sumar la cantidad total pedida
        .order_by('-cantidad_total')[:5]  # Ordenar por cantidad y tomar los 5 primeros
    )

    # Preparar datos para el gráfico
    productos = [item['producto__nombre_prod'] for item in ranking]
    cantidades = [item['cantidad_total'] for item in ranking]

    # Generar el gráfico de torta con Matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        cantidades,
        labels=productos,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors,
    )
    ax.set_title('Distribución de los 5 Pedidos Más Solicitados (Último Mes)', fontsize=14)

    # Guardar el gráfico en un archivo temporal
    temp_image = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    try:
        plt.tight_layout()
        plt.savefig(temp_image.name, format='png')
        plt.close()

        # Crear el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ranking_pedidos.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Ranking de los 5 Pedidos Más Solicitados")
        p.setFont("Helvetica", 12)
        p.drawString(100, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")

        # Agregar el gráfico al PDF
        p.drawImage(temp_image.name, 100, 400, width=400, height=400)  # Ajustar posición y tamaño

        # Cerrar el PDF
        p.showPage()
        p.save()
    finally:
        # Asegurarse de eliminar el archivo temporal
        temp_image.close()
        os.unlink(temp_image.name)

    return response


class ListaCajasView(AdminPermisoMixin, TemplateView):
    template_name = "caja/lista_cajas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todas las cajas
        context['cajas'] = Caja.objects.all().order_by('-fecha_hs_aper_caja')
        return context
    

class DetalleCajaView(AdminPermisoMixin, TemplateView):
    template_name = "caja/detalle_caja.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la caja por ID
        caja_id = self.kwargs['pk']
        caja = Caja.objects.get(pk=caja_id)
        context['caja'] = caja

        # Obtener los pedidos de la caja
        pedidos = Pedidos.objects.filter(caja=caja)

        # Agrupar por producto y calcular cantidades y subtotales
        ventas_por_producto = (
            DetallePedido.objects.filter(pedido__in=pedidos)
            .values('producto__nombre_prod')  # Agrupar por producto
            .annotate(
                cantidad_total=Sum('total_pedido'),
                subtotal=Sum('subtotal')
            )
            .order_by('-cantidad_total')  # Ordenar por cantidad descendente
        )
        context['ventas'] = ventas_por_producto

        # Calcular el total vendido
        total_vendido = sum(item['subtotal'] or 0 for item in ventas_por_producto)
        context['total_vendido'] = total_vendido

        # Agregar el monto inicial
        monto_inicial = caja.monto_inicial_caja or 0
        context['monto_inicial'] = monto_inicial

        # Calcular el efectivo esperado en la caja
        total_egresos = caja.total_egresos or 0
        efectivo_esperado = monto_inicial + total_vendido -  total_egresos
        context['efectivo_esperado'] = efectivo_esperado

        return context