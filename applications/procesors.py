from applications.caja.models import Caja

# proceso para recuperar telefono y correo del  tegistro home

def caja(request):
    try:
        caja = Caja.objects.latest('id')

        return {
            'caja_activa': caja.abierta_caja,
        }
    except:
        return {
            'caja_activa': None,
            
        }