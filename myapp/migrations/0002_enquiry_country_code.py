# Generated by Django 5.0.2 on 2024-02-09 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='country_code',
            field=models.CharField(default='+91', max_length=6),
        ),
    ]