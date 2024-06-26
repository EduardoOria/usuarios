# Generated by Django 4.2.4 on 2024-03-29 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_distribucion_producto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.producto')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.defaultuser')),
            ],
            options={
                'unique_together': {('user', 'producto')},
            },
        ),
    ]
