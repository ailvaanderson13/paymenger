# Generated by Django 3.2.5 on 2021-07-28 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firma', '0001_initial'),
        ('agiota', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agiota',
            name='firma',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='firma.firma'),
        ),
    ]
