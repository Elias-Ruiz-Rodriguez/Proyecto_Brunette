from django.db import models

class Producto(models.Model):
    MENU = 'M'
    GASEOSA = 'G'
    CATEGORIA_CHOICES = [
        (MENU, 'Plato de Comida'),
        (GASEOSA, 'Gaseosa'),
    ]
    
    id_prod = models.AutoField(primary_key=True)
    nombre_prod = models.CharField(max_length=100)
    precio_prod = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Campos solo aplicables para gaseosas
    categoria_prod = models.CharField(
        max_length=1,
        choices=CATEGORIA_CHOICES,
        default=MENU,
    )
    stock_min_prod = models.IntegerField(null=True, blank=True)
    stock_actual_prod = models.IntegerField(default=0, null=True, blank=True)
    punto_reposicion_prod = models.IntegerField(default=0,null=True, blank=True)
    stock_max_prod = models.IntegerField(default=0,null=True, blank=True)
    
    # Campos aplicables para ambos tipos de productos
    existencia_insumo = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Limpiar campos de stock si el producto es de tipo "Menu"
        if self.categoria_prod == self.MENU:
            self.stock_min_prod = None
            self.stock_actual_prod = None
            self.punto_reposicion_prod = None
            self.stock_max_prod = None
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nombre_prod

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_emple = models.IntegerField()  # Cambiar a ForeignKey si tienes un modelo Empleado
    id_caja = models.IntegerField()   # Cambiar a ForeignKey si tienes un modelo Caja
    id_venta = models.IntegerField()   # Cambiar a ForeignKey si tienes un modelo Venta
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
    EFECTIVO = 'efectivo'
    TARJETA = 'tarjeta'
    TIPO_PAGO_CHOICES = [
        (EFECTIVO, 'Efectivo'),
        (TARJETA, 'Tarjeta'),
    ]
    
    tipo_pago = models.CharField(
        max_length=8,
        choices=TIPO_PAGO_CHOICES,
        default=EFECTIVO,  # Establece un valor predeterminado si lo deseas
        null=True, 
        blank=True
    )

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
