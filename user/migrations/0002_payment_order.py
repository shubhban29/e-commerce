# Generated by Django 3.2.4 on 2021-06-28 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_payment_status'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]