# Generated by Django 2.2.7 on 2021-05-20 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CV_APP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postulacion',
            name='finalizado',
            field=models.BooleanField(default=False, verbose_name='Finalizar'),
        ),
    ]
