# Generated by Django 3.0.5 on 2021-01-01 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0003_auto_20210102_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notes.Labels'),
        ),
    ]
