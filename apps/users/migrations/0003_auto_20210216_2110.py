# Generated by Django 3.1.3 on 2021-02-17 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210216_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='access',
        ),
        migrations.RemoveField(
            model_name='user',
            name='refresh',
        ),
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(db_index=True, default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(db_index=True, default=1, max_length=255),
            preserve_default=False,
        ),
    ]