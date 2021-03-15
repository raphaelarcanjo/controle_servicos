# Generated by Django 3.1.7 on 2021-03-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('contato', models.CharField(max_length=20)),
                ('flag_mensageiro', models.BooleanField()),
                ('mensageiro', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=80)),
                ('valor', models.FloatField()),
                ('data', models.DateField()),
                ('pago', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='StatusServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=12)),
            ],
        ),
    ]
