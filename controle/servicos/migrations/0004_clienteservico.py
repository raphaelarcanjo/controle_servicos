# Generated by Django 3.1.7 on 2021-03-15 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0003_andamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.IntegerField()),
                ('servico', models.IntegerField()),
            ],
        ),
    ]
