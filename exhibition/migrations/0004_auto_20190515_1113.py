# Generated by Django 2.1.8 on 2019-05-15 11:13

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exhibition', '0003_auto_20190515_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitiondetailpage',
            name='artist',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='exhibitiondetailpage',
            name='body',
            field=wagtail.core.fields.RichTextField(),
        ),
    ]
