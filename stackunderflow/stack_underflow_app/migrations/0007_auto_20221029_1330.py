# Generated by Django 2.2.10 on 2022-10-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack_underflow_app', '0006_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=10, unique=True, verbose_name='tag name'),
        ),
    ]
