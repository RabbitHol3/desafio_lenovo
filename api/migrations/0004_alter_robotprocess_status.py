# Generated by Django 4.0.4 on 2022-05-24 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_robot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotprocess',
            name='status',
            field=models.CharField(choices=[('running', 'running'), ('stopped', 'stopped')], default='running', max_length=100),
        ),
    ]
