# Generated by Django 3.2.8 on 2021-10-20 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0002_alter_code_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='number',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
