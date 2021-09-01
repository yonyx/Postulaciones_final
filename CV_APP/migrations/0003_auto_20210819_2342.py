# Generated by Django 2.2.7 on 2021-08-20 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CV_APP', '0002_auto_20210520_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='postulacion',
            name='mas15hrs',
            field=models.BooleanField(default=False, verbose_name='+15 hrs'),
        ),
        migrations.AddField(
            model_name='postulacion',
            name='menos15hrs',
            field=models.BooleanField(default=False, verbose_name='-15 hrs'),
        ),
        migrations.AddField(
            model_name='postulacion',
            name='reemplazo',
            field=models.BooleanField(default=False, verbose_name='Reemplazo'),
        ),
    ]