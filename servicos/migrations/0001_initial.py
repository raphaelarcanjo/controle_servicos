# Generated by Django 3.2.6 on 2021-08-26 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('contato', models.CharField(max_length=20)),
                ('flag_mensageiro', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Mensageiro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StatusServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=80)),
                ('valor', models.FloatField()),
                ('data', models.DateField()),
                ('pago', models.BooleanField(default=0)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicos.statusservico')),
            ],
        ),
        migrations.CreateModel(
            name='ClienteServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicos.cliente')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicos.servico')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='mensageiro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='servicos.mensageiro'),
        ),
        migrations.CreateModel(
            name='Andamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicos.servico')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicos.statusservico')),
            ],
        ),
    ]