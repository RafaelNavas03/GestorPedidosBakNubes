import json
import traceback
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import datetime
from Mesero.models import *
from decimal import Decimal
from Mesa.models import Mesas
from Inventario.models import MovimientoInventario

@method_decorator(csrf_exempt, name='dispatch')
class ListaPedidos(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de pedidos con información del cliente y detalle del pedido
            pedidos = Pedidos.objects.filter(estado_del_pedido='O')

            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class ConfirmarPedido(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_pedido = request.POST.get('id_pedido')
                pedido = Pedidos.objects.get(id_pedido=id_pedido)
                precio = "703,00 €"
                precio = precio.replace(",", "").replace("€", "").strip()

                # Reemplaza la coma con un punto si es necesario
                precio = precio.replace(",", ".")

                pedido.precio = Decimal(precio)
                pedido.estado_del_pedido = 'E'
                pedido.save()

                # Cambiar el estado de los movimientos relacionados con este pedido a 0 si son de tipo 'P'
                movimientos_relacionados = MovimientoInventario.objects.filter(id_pedido=id_pedido, tipomovimiento='P', sestado='1')
                for movimiento_relacionado in movimientos_relacionados:
                    movimiento_relacionado.sestado = '0'
                    movimiento_relacionado.save()

                return JsonResponse({'mensaje': 'Pedido confirmado'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)

        
@method_decorator(csrf_exempt, name='dispatch')
class ListaPedidosMesero(View):
    def get(self, request, *args, **kwargs):
        try:
            pedidos = Pedidos.objects.filter(estado_del_pedido__in=['O', 'P'])

            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                # Verifica si el pedido está asociado a una mesa
                mesa_asociada = Pedidosmesa.objects.filter(id_pedido=pedido.id_pedido).first()
                mesa_data = None

                if mesa_asociada:
                    mesa_data = {
                        'id_mesa': mesa_asociada.id_mesa.id_mesa,
                        'observacion': mesa_asociada.id_mesa.observacion,
                        'estado': mesa_asociada.id_mesa.estado,
                        'activa': mesa_asociada.id_mesa.activa,
                        'maxpersonas': mesa_asociada.id_mesa.maxpersonas,
                        'sestado': mesa_asociada.id_mesa.sestado,
                    }

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                    'mesa_asociada': mesa_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
@method_decorator(csrf_exempt, name='dispatch')
class TodosLosPedidos(View):
    def get(self, request, *args, **kwargs):
        try:
            pedidos = Pedidos.objects.all().values()
            pedidos_list = list(pedidos)
            return JsonResponse({'todos_los_pedidos': pedidos_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class TomarPedido(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_usuario = kwargs.get('id_cuenta')
                mesero = Meseros.objects.get(id_cuenta=id_usuario)
                id_mesero = mesero.id_mesero
                id_sucursal = mesero.id_sucursal_id  # Obtener el id_sucursal del mesero

                id_mesa = request.POST.get('id_mesa')
                id_cliente_id = request.POST.get('id_cliente')
                fecha_pedido = datetime.now()
                tipo_de_pedido = request.POST.get('tipo_de_pedido')
                metodo_de_pago = request.POST.get('metodo_de_pago')
                puntos = request.POST.get('puntos')
                fecha_entrega = request.POST.get('fecha_entrega', None)
                estado_del_pedido = request.POST.get('estado_del_pedido')
                observacion_del_cliente = request.POST.get('observacion_del_cliente')
                
                cliente_instance = get_object_or_404(Clientes, id_cliente=id_cliente_id)

                nuevo_pedido = Pedidos.objects.create(
                    id_cliente=cliente_instance,
                    precio=0,
                    tipo_de_pedido=tipo_de_pedido,
                    metodo_de_pago=metodo_de_pago,
                    puntos=puntos,
                    fecha_pedido=fecha_pedido,
                    fecha_entrega=fecha_entrega,
                    estado_del_pedido=estado_del_pedido,
                    observacion_del_cliente=observacion_del_cliente,
                )

                mesero_instance = get_object_or_404(Meseros, id_mesero=id_mesero)
                mesa_instance = get_object_or_404(Mesas, id_mesa=id_mesa)
                Pedidosmesa.objects.create(
                    id_mesero=mesero_instance,
                    id_mesa=mesa_instance,
                    id_pedido=nuevo_pedido,
                )

                detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')
                detalles_pedido = json.loads(detalles_pedido_raw)

                total_precio_pedido = Decimal(0)
                total_descuento = Decimal(0)

                # Crear los detalles de detalle de pedido
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    precio_unitario = Decimal(detalle_pedido_data['precio_unitario'])
                    # Impuesto establecido en 0 para evitar que se calcule
                    impuesto = Decimal(0)
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))

                    precio_total_detalle = (precio_unitario + impuesto) * cantidad - descuento
                    total_precio_pedido += precio_total_detalle
                    total_descuento += descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_producto=producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_combo=combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )

                # Calcular el subtotal y el total del pedido
                subtotal = total_precio_pedido - total_descuento  # Subtotal = Total - Descuento

                # El impuesto en la factura se calcula correctamente
                iva_factura = subtotal * Decimal('0.12')
                a_pagar = subtotal + iva_factura  # A pagar = Subtotal + 12% IVA

                # Guardar el monto a pagar en lugar del total
                nuevo_pedido.precio = a_pagar
                nuevo_pedido.save()

                # Crear la factura asociada al pedido
                try:
                    numero_factura, numero_factura_desde, numero_factura_hasta = Codigosri.obtener_proximo_numero_factura(id_mesero, id_sucursal)
                except ValueError as e:
                    numero_factura = None  # No se pudo obtener el número de factura
                    numero_factura_desde = None
                    numero_factura_hasta = None

                nueva_factura = Factura.objects.create(
                    id_pedido=nuevo_pedido,
                    id_cliente=cliente_instance,
                    id_mesero=mesero_instance,
                    total=total_precio_pedido,
                    iva=iva_factura,
                    descuento=total_descuento,
                    subtotal=subtotal,
                    a_pagar=a_pagar,
                    codigo_factura=numero_factura,
                    codigo_autorizacion=Codigoautorizacion.obtener_codigo_autorizacion_valido(),
                    fecha_emision=datetime.now(),
                    numero_factura_desde=numero_factura_desde,  # Asigna el valor devuelto por el método
                    numero_factura_hasta=numero_factura_hasta,  # Asigna el valor devuelto por el método
                )

                # Crear los detalles de la factura
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    precio_unitario = Decimal(detalle_pedido_data['precio_unitario'])
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))
                    valor = (precio_unitario * cantidad) - descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        id_producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_producto=id_producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        id_combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_combo=id_combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )

                return JsonResponse({'mensaje': 'Pedido y factura creados con éxito'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No se encontró ningún registro en Codigosri'}, status=400)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class TomarPedidoSinMesa(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_usuario = kwargs.get('id_cuenta')
                mesero = Meseros.objects.get(id_cuenta=id_usuario)
                id_mesero = mesero.id_mesero
                id_sucursal = mesero.id_sucursal_id  # Obtener el id_sucursal del mesero
                id_cliente_id = request.POST.get('id_cliente')
                fecha_pedido = datetime.now()
                tipo_de_pedido = request.POST.get('tipo_de_pedido')
                metodo_de_pago = request.POST.get('metodo_de_pago')
                puntos = request.POST.get('puntos')
                fecha_entrega = request.POST.get('fecha_entrega', None)
                estado_del_pedido = request.POST.get('estado_del_pedido')
                observacion_del_cliente = request.POST.get('observacion_del_cliente')
                
                cliente_instance = get_object_or_404(Clientes, id_cliente=id_cliente_id)

                nuevo_pedido = Pedidos.objects.create(
                    id_cliente=cliente_instance,
                    precio=0,
                    tipo_de_pedido=tipo_de_pedido,
                    metodo_de_pago=metodo_de_pago,
                    puntos=puntos,
                    fecha_pedido=fecha_pedido,
                    fecha_entrega=fecha_entrega,
                    estado_del_pedido=estado_del_pedido,
                    observacion_del_cliente=observacion_del_cliente,
                )
                mesero_instance = get_object_or_404(Meseros, id_mesero=id_mesero)
                detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')
                detalles_pedido = json.loads(detalles_pedido_raw)
                total_precio_pedido = Decimal(0)
                total_descuento = Decimal(0)
                # Crear los detalles de detalle de pedido
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    precio_unitario = Decimal(detalle_pedido_data['precio_unitario'])
                    # Impuesto establecido en 0 para evitar que se calcule
                    impuesto = Decimal(0)
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))

                    precio_total_detalle = (precio_unitario + impuesto) * cantidad - descuento
                    total_precio_pedido += precio_total_detalle
                    total_descuento += descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_producto=producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_combo=combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )

                # Calcular el subtotal y el total del pedido
                subtotal = total_precio_pedido - total_descuento  # Subtotal = Total - Descuento
                iva_factura = subtotal * Decimal('0.12')
                a_pagar = subtotal + iva_factura  # A pagar = Subtotal + 12% IVA
                nuevo_pedido.precio = a_pagar
                nuevo_pedido.save()

                # Crear la factura asociada al pedido
                numero_factura, numero_factura_desde, numero_factura_hasta = Codigosri.obtener_proximo_numero_factura(id_mesero, id_sucursal)
                nueva_factura = Factura.objects.create(
                    id_pedido=nuevo_pedido,
                    id_cliente=cliente_instance,
                    id_mesero=mesero_instance,
                    total=total_precio_pedido,
                    iva=iva_factura,
                    descuento=total_descuento,
                    subtotal=subtotal,
                    a_pagar=a_pagar,
                    codigo_factura=numero_factura,
                    codigo_autorizacion=Codigoautorizacion.obtener_codigo_autorizacion_valido(),
                    fecha_emision=datetime.now(),
                    numero_factura_desde=numero_factura_desde,  # Asigna el valor devuelto por el método
                    numero_factura_hasta=numero_factura_hasta,  # Asigna el valor devuelto por el método
                )



                # Crear los detalles de la factura
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    precio_unitario = Decimal(detalle_pedido_data['precio_unitario'])
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))
                    valor = (precio_unitario * cantidad) - descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        id_producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_producto=id_producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        id_combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_combo=id_combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )

                return JsonResponse({'mensaje': 'Pedido y factura creados con éxito'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)
def ver_factura(request, id_pedido):
    print("ID de pedido recibido:", id_pedido)
    try:
        print('aver')
        factura = Factura.objects.get(id_pedido_id=id_pedido)
        detalles_factura = DetalleFactura.objects.filter(id_factura_id=factura.id_factura).values()

        detalles_factura_list = list(detalles_factura)
        id_cliente = factura.id_cliente_id
        print('aver')
        # Obtener información del pedido
        pedido = Pedidos.objects.get(pk=id_pedido)
        print('averx')
        tipo_de_pedido = pedido.tipo_de_pedido
        print('averx1')
        metodo_de_pago = pedido.metodo_de_pago
        print('aver2')
        # Obtener la información de la factura
        codigo_autorizacion_sri = factura.codigo_autorizacion
        print('averx3')
        codigo_autorizacion_obj = Codigoautorizacion.objects.get(codigo_autorizacion=codigo_autorizacion_sri)
        print('averx4')
        fecha_autorizacion = codigo_autorizacion_obj.fecha_autorizacion
        print('averx5')
        fecha_vencimiento = codigo_autorizacion_obj.fecha_vencimiento
        print('aver3')
        # Obtener la numeración desde el modelo Codigosri
        numeracion = f"{factura.numero_factura_desde}-{factura.numero_factura_hasta}"
        print('aver4')
        factura_data = {
            'id_factura': factura.id_factura,
            'id_cliente': id_cliente,
            'codigo_factura': factura.codigo_factura,
            'codigo_autorizacion_sri': codigo_autorizacion_sri,
            'autorizacion': fecha_autorizacion,
            'vencimiento': fecha_vencimiento,
            'numeracion': numeracion,
            'fecha_emision': factura.fecha_emision,
            'a_pagar': factura.a_pagar,
            'iva': factura.iva,
            'total': factura.total,
            'descuento': factura.descuento,
            'subtotal': factura.subtotal,
            'tipo_de_pedido': tipo_de_pedido,
            'metodo_de_pago': metodo_de_pago,  
            'detalles_factura': detalles_factura_list,
        }
        print('aver5')
        return JsonResponse(factura_data)
    except Factura.DoesNotExist:
        return JsonResponse({'error': 'La factura no existe'}, status=404)


def pedidos_del_mesero(request, id_mesa, **kwargs):
    try:
        id_usuario = kwargs.get('id_cuenta')
        id_mesero = Meseros.objects.get(id_cuenta=id_usuario)
        
        # Obtener todos los pedidos asociados al mesero y a la mesa
        pedidos_del_mesero = Pedidosmesa.objects.filter(id_mesero=id_mesero, id_mesa=id_mesa)

        # Inicializar una lista para almacenar la información de los pedidos
        pedidos_info = []

        # Iterar sobre cada pedido asociado al mesero y a la mesa
        for pedido_mesa in pedidos_del_mesero:
            # Obtener la información del pedido
            pedido_info = {
                'id_pedido': pedido_mesa.id_pedido.id_pedido,
                'id_mesa': pedido_mesa.id_mesa.id_mesa,
                'fecha_pedido': pedido_mesa.id_pedido.fecha_pedido,
                # Otros campos del pedido que quieras mostrar
            }
            pedidos_info.append(pedido_info)

        return JsonResponse({'pedidos_del_mesero': pedidos_info})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
class ObtenerMeseroView(View):
    def get(self, request, *args, **kwargs):
        try:
            id_usuario = kwargs.get('id_usuario')
            
            if id_usuario:
                # Si se proporciona un ID de usuario, intenta obtener ese usuario
                cuenta = get_object_or_404(Cuenta, id_cuenta=id_usuario)
                mesero = get_object_or_404(Meseros, id_cuenta=cuenta)

                mesero_data = {
                    'id_mesero': mesero.id_mesero,
                    'id_sucursal': mesero.id_sucursal.id_sucursal,
                    'id_administrador': mesero.id_administrador.id_administrador,
                    'telefono': mesero.telefono,
                    'apellido': mesero.apellido,
                    'nombre': mesero.nombre,
                    'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                    'id_cuenta': mesero.id_cuenta.id_cuenta if mesero.id_cuenta else None,
                    'sestado': mesero.sestado,
                }

                return JsonResponse({'mesero': mesero_data})
            else:
                # Si no se proporciona un ID de usuario, retorna un error
                return JsonResponse({'error': 'ID de usuario no proporcionado'}, status=400)

        except Cuenta.DoesNotExist:
            return JsonResponse({'error': 'Cuenta no encontrada'}, status=404)

        except Meseros.DoesNotExist:
            return JsonResponse({'error': 'Mesero no encontrado'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class ListaMeseros(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de meseros
            meseros = Meseros.objects.all()

            # Formatea los datos
            data = []
            for mesero in meseros:
                mesero_data = {
                    'id_mesero': mesero.id_mesero,
                    'id_sucursal': mesero.id_sucursal.id_sucursal,
                    'id_administrador': mesero.id_administrador.id_administrador,
                    'nombre': mesero.nombre,
                    'apellido': mesero.apellido,
                    'telefono': mesero.telefono,
                    'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                    'sestado': mesero.sestado,
                }
                data.append(mesero_data)

            return JsonResponse({'meseros': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ListaFacturas(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de facturas
            facturas = Factura.objects.all()

            # Formatea los datos
            data = []
            for factura in facturas:
                factura_data = {
                    'id_factura': factura.id_factura,
                    'id_pedido': factura.id_pedido.id_pedido if factura.id_pedido else None,
                    'id_cliente': factura.id_cliente.id_cliente if factura.id_cliente else None,
                    'id_mesero': factura.id_mesero.id_mesero if factura.id_mesero else None,
                    'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S') if factura.fecha_emision else None,
                    'total': str(factura.total),
                    'iva': str(factura.iva) if factura.iva else None,
                    'descuento': str(factura.descuento) if factura.descuento else None,
                    'subtotal': str(factura.subtotal) if factura.subtotal else None,
                    'a_pagar': str(factura.a_pagar) if factura.a_pagar else None,
                    'codigo_factura': factura.codigo_factura,
                    'codigo_autorizacion': factura.codigo_autorizacion,
                    'numero_factura_desde': factura.numero_factura_desde,
                    'numero_factura_hasta': factura.numero_factura_hasta,
                }
                data.append(factura_data)

            return JsonResponse({'facturas': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)