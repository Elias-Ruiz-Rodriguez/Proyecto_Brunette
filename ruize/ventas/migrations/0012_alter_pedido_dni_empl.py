# Generated by Django 5.1.3 on 2024-11-24 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alter_empleados_rol_empl'),
        ('ventas', '0011_remove_pedido_id_emple_pedido_dni_empl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='dni_empl',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.login'),
        ),
    ]
