# Generated by Django 3.2.5 on 2021-07-31 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_cliente_agiota'),
        ('emprestimo', '0007_alter_emprestimo_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cliente.cliente'),
        ),
    ]
