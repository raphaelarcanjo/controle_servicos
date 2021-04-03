# Generated by Django 3.1.7 on 2021-04-03 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0005_auto_20210317_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='flag_mensageiro',
            field=models.BooleanField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='mensageiro',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='pago',
            field=models.BooleanField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='status',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
