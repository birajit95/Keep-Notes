# Generated by Django 3.0.8 on 2021-01-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210107_2349'),
        ('Notes', '0018_notes_trashedat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='collaborator',
        ),
        migrations.AddField(
            model_name='notes',
            name='collaborator',
            field=models.ManyToManyField(related_name='collaborator', to='authentication.User'),
        ),
    ]
