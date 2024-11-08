from django.db import models

class Producto(models.Model):
    id_prod = models.AutoField(primary_key=True)
    nombre_prod = models.CharField(max_length=100)
    precio_prod = models.DecimalField(max_digits=10, decimal_places=2)
    stock_min_prod = models.IntegerField()
    stock_actual_prod = models.IntegerField()
    punto_reposicion_prod = models.IntegerField()
    stock_max_prod = models.IntegerField()
    existencia_insumo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_prod

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_emple = models.IntegerField()  # Cambiar a ForeignKey si tienes un modelo Empleado
    id_caja = models.IntegerField()   # Cambiar a ForeignKey si tienes un modelo Caja
    id_veta = models.IntegerField()   # Cambiar a ForeignKey si tienes un modelo Venta
    generado_ped = models.BooleanField(default=False)
    fecha_gene_ped = models.DateField(null=True, blank=True)
    hora_gen_ped = models.TimeField(null=True, blank=True)
    proceso_ped = models.BooleanField(default=False)
    fecha_pro_ped = models.DateField(null=True, blank=True)
    hora_pro_ped = models.TimeField(null=True, blank=True)
    listo_ped = models.BooleanField(default=False)
    fecha_lis_ped = models.DateField(null=True, blank=True)
    hora_lis_ped = models.TimeField(null=True, blank=True)
    entregado_ped = models.BooleanField(default=False)
    fecha_ent_ped = models.DateField(null=True, blank=True)
    hora_ent_ped = models.TimeField(null=True, blank=True)
    pagado_ped = models.BooleanField(default=False)
    fecha_pago = models.DateField(null=True, blank=True)
    hora_pago = models.TimeField(null=True, blank=True)
    tipo_pago = models.CharField(max_length=50, null=True, blank=True)  # Ejemplo: Efectivo, Tarjeta

    def __str__(self):
        return f"Pedido {self.id_pedido}"

class DetallePedido(models.Model):
    id_det_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_uni_ped = models.DecimalField(max_digits=10, decimal_places=2)
    cant_ped = models.IntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    total_ped = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id_det_pedido} del Pedido {self.id_pedido.id_pedido}"
