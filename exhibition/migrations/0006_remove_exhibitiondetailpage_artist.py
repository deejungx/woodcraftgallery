# Generated by Django 2.1.8 on 2019-05-22 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exhibition', '0005_auto_20190522_0455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exhibitiondetailpage',
            name='artist',
        ),
    ]
