# Generated by Django 2.2 on 2020-10-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_auto_20201029_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Gambar Thumbnail'),
        ),
    ]
