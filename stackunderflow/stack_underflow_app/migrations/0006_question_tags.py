# Generated by Django 2.2.10 on 2022-10-29 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack_underflow_app', '0005_auto_20221029_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='stack_underflow_app.Tag'),
        ),
    ]