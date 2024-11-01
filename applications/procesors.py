from applications.caja.models import Caja

# proceso para recuperar telefono y correo del  tegistro home

def caja(request):
    try:
        caja = Caja.objects.latest('id')
        # caja = Caja.objects.filter(
        #     abierta_caja = True,
        #     user__full_name = request.user.full_name
        # )
        user_caja = caja.user.full_name
        return {
            'caja_activa': caja.abierta_caja,
            'caja_activa_usuario': user_caja  # Agrega el usuario que tiene la caja activa

        }
    except:
        return {
            'caja_activa': None,
            'caja_activa_usuario': None,
        }
    



    # def caja(request):
    # try:
    #     caja = Caja.objects.latest('id')
    #     return {
    #         'caja_activa': caja.abierta_caja,
    #         'caja_activa_usuario': caja.usuario.get_full_name() if caja.abierta_caja else None,  # Agrega el usuario que tiene la caja activa
    #     }
    # except Caja.DoesNotExist:
    #     return {
    #         'caja_activa': None,
    #         'caja_activa_usuario': None,
    #     }
