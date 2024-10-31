from django.db import models

class Empleados(models.Model):
    dni_empl = models.CharField(primary_key=True, max_length=20)
    nombre_empl = models.CharField(max_length=100)
    apellido_empl = models.CharField(max_length=100)
    domicilio_empl = models.TextField()
    telefono_empl = models.CharField(max_length=15)
    correo_empl = models.EmailField()

class Login(models.Model):
    id_login = models.BigAutoField(primary_key=True)
    dni_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    ultimo_acceso = models.DateTimeField()
    hs_login = models.TimeField()

class Caja(models.Model):
    id_caja = models.BigAutoField(primary_key=True)
    dni_empl = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    abierta_caja = models.BooleanField()
    fecha_hs_apertura = models.DateTimeField()
    fecha_hs_cierre = models.DateTimeField()
    monto_inicial_caja = models.DecimalField(max_digits=10, decimal_places=2)
    total_ingresos_caja = models.DecimalField(max_digits=10, decimal_places=2)
    total_caja = models.DecimalField(max_digits=10, decimal_places=2)

class Proveedores(models.Model):
    id_prov = models.BigAutoField(primary_key=True)
    nombre_prov = models.CharField(max_length=100)
    tipo_prov = models.CharField(max_length=50)
    telefono_prov = models.CharField(max_length=15)
    correo_prov = models.EmailField()
    direccion_prov = models.TextField()

class Compras(models.Model):
    id_comp = models.BigAutoField(primary_key=True)
    id_caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    id_prov = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    fecha_comp = models.DateField()
    monto_comp = models.DecimalField(max_digits=10, decimal_places=2)
    nro_comp = models.CharField(max_length=50)

class Productos(models.Model):
    id_prod = models.BigAutoField(primary_key=True)
    nombre_prod = models.CharField(max_length=100)
    precio_prod = models.DecimalField(max_digits=10, decimal_places=2)
    stock_min_prod = models.IntegerField()
    stock_actual_prod = models.IntegerField()
    punto_reposicion_prod = models.IntegerField()
    stock_max_prod = models.IntegerField()
    existencia_insumo = models.BooleanField()

class DetalleCompra(models.Model):
    id_det_comp = models.BigAutoField(primary_key=True)
    id_comp = models.ForeignKey(Compras, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad_prod = models.IntegerField()
    precio_uni_prod = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total_comp = models.DecimalField(max_digits=10, decimal_places=2)
    total_comp = models.DecimalField(max_digits=10, decimal_places=2)

class Clientes(models.Model):
    id_cli = models.BigAutoField(primary_key=True)
    nombre_cli = models.CharField(max_length=100)
    apellido_cli = models.CharField(max_length=100)
    cuit_cli = models.CharField(max_length=20)
    tel_cli = models.CharField(max_length=15)

class Ventas(models.Model):
    id_venta = models.BigAutoField(primary_key=True)
    id_cli = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    fecha_venta = models.DateField()
    hora_venta = models.TimeField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    venta_realizada = models.BooleanField()

class DetalleVenta(models.Model):
    id_det_venta = models.BigAutoField(primary_key=True)
    id_venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cant_prod_venta = models.IntegerField()
    subtotal_det = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class PagoImpuestos(models.Model):
    id_pago = models.BigAutoField(primary_key=True)
    id_caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    id_impuestos = models.ForeignKey('Impuestos', on_delete=models.CASCADE)
    fecha_hs_pago = models.DateTimeField()

class Impuestos(models.Model):
    id_impuesto = models.BigAutoField(primary_key=True)
    fecha_imp = models.DateField()
    fecha_venc_imp = models.DateField()
    monto_imp = models.DecimalField(max_digits=10, decimal_places=2)

class ProvProductos(models.Model):
    id_prov = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Productos, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_prov', 'id_prod'),)

class Pedidos(models.Model):
    id_ped = models.BigAutoField(primary_key=True)
    id_emple = models.ForeignKey(Empleados, on_delete=models.CASCADE)