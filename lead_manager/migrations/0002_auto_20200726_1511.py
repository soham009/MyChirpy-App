# Generated by Django 2.2 on 2020-07-26 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leads',
            name='website',
            field=models.CharField(blank=True, max_length=264),
        ),
    ]
