# Generated by Django 4.0 on 2022-01-24 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoFill', '0014_alter_dmgroupmodel_subjectcount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='perdmgroupdmlistmodel',
            name='last_sent_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='perdmgroupdmlistmodel',
            name='last_sent_user',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]