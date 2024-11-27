# Generated by Django 5.1.3 on 2024-11-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(choices=[('standard', 'Entrega Estándar (5.00€)'), ('express', 'Entrega Express (10.00€)'), ('free', 'Envío Gratuito')], default='standard', max_length=20),
        ),
    ]
