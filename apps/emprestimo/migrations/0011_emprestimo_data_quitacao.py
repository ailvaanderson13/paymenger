# Generated by Django 3.2.5 on 2021-08-03 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprestimo', '0010_emprestimo_num_parcela'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='data_quitacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
