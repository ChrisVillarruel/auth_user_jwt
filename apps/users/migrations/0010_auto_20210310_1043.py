# Generated by Django 3.1.3 on 2021-03-10 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.BooleanField(default=True, verbose_name='Este campo no lo puede modificar el administrador.'),
        ),
    ]
