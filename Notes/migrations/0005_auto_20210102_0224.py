# Generated by Django 3.0.5 on 2021-01-01 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0004_auto_20210102_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='label',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='Notes.Labels'),
        ),
    ]
