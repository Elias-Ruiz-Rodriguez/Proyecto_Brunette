# Generated by Django 5.1.3 on 2024-11-27 23:39

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0013_alter_historialcaja_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')], max_length=10)),
                ('monto', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caja.caja')),
            ],
        ),
    ]
