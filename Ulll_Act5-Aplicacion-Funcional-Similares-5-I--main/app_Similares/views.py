# app_Similares/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import (
    Cliente, Proveedor, Medicamento, Producto, Empleado, Venta
)
from django.utils import timezone
import random
import string

# === INICIO ===
def inicio_similares(request):
    total_ventas = Venta.objects.count()
    total_medicamentos = Medicamento.objects.count()
    total_productos = Producto.objects.count()
    total_empleados = Empleado.objects.filter(activo=True).count()
    return render(request, 'app_Similares/inicio.html', {
        'total_ventas': total_ventas,
        'total_medicamentos': total_medicamentos,
        'total_productos': total_productos,
        'total_empleados': total_empleados,
    })

# === CLIENTES ===
def ver_clientes(request):
    clientes = Cliente.objects.all().order_by('apellido')
    return render(request, 'app_Similares/clientes/ver_clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            email=request.POST['email'],
            telefono=request.POST['telefono'],
            direccion=request.POST['direccion'],
            fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
        )
        return redirect('ver_clientes')
    return render(request, 'app_Similares/clientes/agregar_cliente.html')

def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'app_Similares/clientes/actualizar_cliente.html', {'cliente': cliente})

def realizar_actualizacion_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.email = request.POST['email']
        cliente.telefono = request.POST['telefono']
        cliente.direccion = request.POST['direccion']
        cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        cliente.save()
        return redirect('ver_clientes')
    return redirect('actualizar_cliente', pk=pk)

def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('ver_clientes')

# === PROVEEDORES ===
def ver_proveedores(request):
    proveedores = Proveedor.objects.filter(activo=True).order_by('nombre_empresa')
    return render(request, 'app_Similares/proveedores/ver_proveedores.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre_empresa=request.POST['nombre_empresa'],
            contacto=request.POST['contacto'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            direccion=request.POST['direccion'],
            rfc=request.POST['rfc'],
        )
        return redirect('ver_proveedores')
    return render(request, 'app_Similares/proveedores/agregar_proveedor.html')

def actualizar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'app_Similares/proveedores/actualizar_proveedor.html', {'proveedor': proveedor})

def realizar_actualizacion_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.nombre_empresa = request.POST['nombre_empresa']
        proveedor.contacto = request.POST['contacto']
        proveedor.telefono = request.POST['telefono']
        proveedor.email = request.POST['email']
        proveedor.direccion = request.POST['direccion']
        proveedor.rfc = request.POST['rfc']
        proveedor.activo = 'activo' in request.POST
        proveedor.save()
        return redirect('ver_proveedores')
    return redirect('actualizar_proveedor', pk=pk)

def borrar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.activo = False
    proveedor.save()
    return redirect('ver_proveedores')

# === MEDICAMENTOS ===
def ver_medicamentos(request):
    medicamentos = Medicamento.objects.select_related('proveedor').all().order_by('nombre')
    return render(request, 'app_Similares/medicamentos/ver_medicamentos.html', {'medicamentos': medicamentos})

def agregar_medicamento(request):
    proveedores = Proveedor.objects.filter(activo=True)
    if request.method == 'POST':
        Medicamento.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            laboratorio=request.POST['laboratorio'],
            precio=request.POST['precio'],
            stock=request.POST['stock'],
            fecha_vencimiento=request.POST['fecha_vencimiento'],
            codigo_barras=request.POST['codigo_barras'],
            proveedor_id=request.POST['proveedor'],
        )
        return redirect('ver_medicamentos')
    return render(request, 'app_Similares/medicamentos/agregar_medicamento.html', {'proveedores': proveedores})

def actualizar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'app_Similares/medicamentos/actualizar_medicamento.html', {
        'medicamento': medicamento, 'proveedores': proveedores
    })

def realizar_actualizacion_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        medicamento.nombre = request.POST['nombre']
        medicamento.descripcion = request.POST['descripcion']
        medicamento.laboratorio = request.POST['laboratorio']
        medicamento.precio = request.POST['precio']
        medicamento.stock = request.POST['stock']
        medicamento.fecha_vencimiento = request.POST['fecha_vencimiento']
        medicamento.codigo_barras = request.POST['codigo_barras']
        medicamento.proveedor_id = request.POST['proveedor']
        medicamento.save()
        return redirect('ver_medicamentos')
    return redirect('actualizar_medicamento', pk=pk)

def borrar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    medicamento.delete()
    return redirect('ver_medicamentos')

# === PRODUCTOS ===
def ver_productos(request):
    productos = Producto.objects.select_related('proveedor').all().order_by('nombre')
    return render(request, 'app_Similares/productos/ver_productos.html', {'productos': productos})

def agregar_producto(request):
    proveedores = Proveedor.objects.filter(activo=True)
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            categoria=request.POST['categoria'],
            precio=request.POST['precio'],
            stock=request.POST['stock'],
            proveedor_id=request.POST['proveedor'],
            codigo_barras=request.POST['codigo_barras'],
        )
        return redirect('ver_productos')
    return render(request, 'app_Similares/productos/agregar_producto.html', {'proveedores': proveedores})

def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'app_Similares/productos/actualizar_producto.html', {
        'producto': producto, 'proveedores': proveedores
    })

def realizar_actualizacion_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.categoria = request.POST['categoria']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.proveedor_id = request.POST['proveedor']
        producto.codigo_barras = request.POST['codigo_barras']
        producto.save()
        return redirect('ver_productos')
    return redirect('actualizar_producto', pk=pk)

def borrar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('ver_productos')

# === EMPLEADOS ===
def ver_empleados(request):
    empleados = Empleado.objects.filter(activo=True).order_by('apellido')
    return render(request, 'app_Similares/empleados/ver_empleados.html', {'empleados': empleados})

def agregar_empleado(request):
    if request.method == 'POST':
        Empleado.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            puesto=request.POST['puesto'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
        )
        return redirect('ver_empleados')
    return render(request, 'app_Similares/empleados/agregar_empleado.html')

def actualizar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return render(request, 'app_Similares/empleados/actualizar_empleado.html', {'empleado': empleado})

def realizar_actualizacion_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.puesto = request.POST['puesto']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.telefono = request.POST['telefono']
        empleado.email = request.POST['email']
        empleado.activo = 'activo' in request.POST
        empleado.save()
        return redirect('ver_empleados')
    return redirect('actualizar_empleado', pk=pk)

def borrar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    empleado.activo = False
    empleado.save()
    return redirect('ver_empleados')

# === VENTAS ===
def generar_factura():
    return 'FAC-' + ''.join(random.choices(string.digits, k=6))

def ver_ventas(request):
    ventas = Venta.objects.select_related('cliente', 'empleado').prefetch_related('medicamentos', 'productos').all().order_by('-fecha_venta')
    return render(request, 'app_Similares/ventas/ver_ventas.html', {'ventas': ventas})

def agregar_venta(request):
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.filter(activo=True)
    medicamentos = Medicamento.objects.filter(stock__gt=0)
    productos = Producto.objects.filter(stock__gt=0)

    if request.method == 'POST':
        with transaction.atomic():
            venta = Venta.objects.create(
                cliente_id=request.POST['cliente'],
                empleado_id=request.POST['empleado'],
                total=0,
                metodo_pago=request.POST['metodo_pago'],
                numero_factura=generar_factura(),
                observaciones=request.POST.get('observaciones', ''),
                estado='COMPLETADA'
            )

            total = 0
            # Medicamentos
            meds = request.POST.getlist('medicamentos')
            for med_id in meds:
                med = Medicamento.objects.get(id=med_id)
                venta.medicamentos.add(med)
                total += med.precio
                med.stock -= 1
                med.save()

            # Productos
            prods = request.POST.getlist('productos')
            for prod_id in prods:
                prod = Producto.objects.get(id=prod_id)
                venta.productos.add(prod)
                total += prod.precio
                prod.stock -= 1
                prod.save()

            venta.total = total
            venta.save()
            return redirect('ver_ventas')

    return render(request, 'app_Similares/ventas/agregar_venta.html', {
        'clientes': clientes,
        'empleados': empleados,
        'medicamentos': medicamentos,
        'productos': productos,
    })

def actualizar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'app_Similares/ventas/actualizar_venta.html', {'venta': venta})

def realizar_actualizacion_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.estado = request.POST['estado']
        venta.observaciones = request.POST.get('observaciones', '')
        venta.save()
        return redirect('ver_ventas')
    return redirect('actualizar_venta', pk=pk)

def borrar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    venta.delete()
    return redirect('ver_ventas')