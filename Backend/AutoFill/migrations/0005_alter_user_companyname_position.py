# Generated by Django 4.0 on 2022-03-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoFill', '0004_user_companyname_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='companyname_position',
            field=models.CharField(blank=True, default='前', max_length=50, null=True),
        ),
    ]