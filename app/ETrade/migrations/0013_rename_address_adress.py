# Generated by Django 5.0.4 on 2024-04-15 11:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ETrade', '0012_alter_profil_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Address',
            new_name='Adress',
        ),
    ]
