# Generated by Django 4.0.6 on 2024-03-06 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ref',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
