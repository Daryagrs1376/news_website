# Generated by Django 5.1.3 on 2024-11-25 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_delete_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subtitle',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
