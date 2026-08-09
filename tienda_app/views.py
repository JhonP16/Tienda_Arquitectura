from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .infra.factories import PaymentFactory
from .services import CompraRapidaService, CompraService


class CompraView(View):
    """
    CBV: Vista Basada en Clases.
    Actúa como un "Portero": recibe la petición y delega al servicio.
    """

    template_name = 'tienda_app/compra.html'

    def setup_service(self):
        # ANTES: gateway = BancoNacionalProcesador()
        # AHORA: Delegación total a la Fábrica
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(
                request,
                self.template_name,
                {
                    'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                    'total': total,
                },
            )
        except (ValueError, Exception) as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)

"""
CompraRapidaView vía CBV
"""
class CompraRapidaView(View):

    template_name = 'tienda_app/compra_rapida.html'

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraRapidaService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.procesar(libro_id)
        except ValueError as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)

        if total is None:
            return render(request, self.template_name, {'error': 'Pago rechazado.'}, status=400)

        return render(request, self.template_name, {
            'mensaje_exito': f"¡Compra exitosa! Total: ${total}",
            'total': total,
        })