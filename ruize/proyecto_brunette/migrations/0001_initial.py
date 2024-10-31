# Generated by Django 5.1.2 on 2024-10-31 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id_caja', models.BigAutoField(primary_key=True, serialize=False)),
                ('abierta_caja', models.BooleanField()),
                ('fecha_hs_apertura', models.DateTimeField()),
                ('fecha_hs_cierre', models.DateTimeField()),
                ('monto_inicial_caja', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_ingresos_caja', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_caja', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id_cli', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_cli', models.CharField(max_length=100)),
                ('apellido_cli', models.CharField(max_length=100)),
                ('cuit_cli', models.CharField(max_length=20)),
                ('tel_cli', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('dni_empl', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_empl', models.CharField(max_length=100)),
                ('apellido_empl', models.CharField(max_length=100)),
                ('domicilio_empl', models.TextField()),
                ('telefono_empl', models.CharField(max_length=15)),
                ('correo_empl', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Impuestos',
            fields=[
                ('id_impuesto', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_imp', models.DateField()),
                ('fecha_venc_imp', models.DateField()),
                ('monto_imp', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id_prod', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_prod', models.CharField(max_length=100)),
                ('precio_prod', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_min_prod', models.IntegerField()),
                ('stock_actual_prod', models.IntegerField()),
                ('punto_reposicion_prod', models.IntegerField()),
                ('stock_max_prod', models.IntegerField()),
                ('existencia_insumo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id_prov', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_prov', models.CharField(max_length=100)),
                ('tipo_prov', models.CharField(max_length=50)),
                ('telefono_prov', models.CharField(max_length=15)),
                ('correo_prov', models.EmailField(max_length=254)),
                ('direccion_prov', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id_comp', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_comp', models.DateField()),
                ('monto_comp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nro_comp', models.CharField(max_length=50)),
                ('id_caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.caja')),
                ('id_prov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.proveedores')),
            ],
        ),
        migrations.AddField(
            model_name='caja',
            name='dni_empl',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.empleados'),
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id_login', models.BigAutoField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=50)),
                ('contraseña', models.CharField(max_length=50)),
                ('ultimo_acceso', models.DateTimeField()),
                ('hs_login', models.TimeField()),
                ('dni_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.empleados')),
            ],
        ),
        migrations.CreateModel(
            name='PagoImpuestos',
            fields=[
                ('id_pago', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_hs_pago', models.DateTimeField()),
                ('id_caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.caja')),
                ('id_impuestos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.impuestos')),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id_ped', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_emple', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.empleados')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id_det_comp', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad_prod', models.IntegerField()),
                ('precio_uni_prod', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sub_total_comp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_comp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.compras')),
                ('id_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id_venta', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_venta', models.DateField()),
                ('hora_venta', models.TimeField()),
                ('total_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('venta_realizada', models.BooleanField()),
                ('id_caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.caja')),
                ('id_cli', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.clientes')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id_det_venta', models.BigAutoField(primary_key=True, serialize=False)),
                ('cant_prod_venta', models.IntegerField()),
                ('subtotal_det', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.productos')),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.ventas')),
            ],
        ),
        migrations.CreateModel(
            name='ProvProductos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.productos')),
                ('id_prov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto_brunette.proveedores')),
            ],
            options={
                'unique_together': {('id_prov', 'id_prod')},
            },
        ),
    ]
