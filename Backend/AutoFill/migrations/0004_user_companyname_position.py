# Generated by Django 4.0 on 2022-03-05 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoFill', '0003_dmtextsetmodel_dmtitle_dmtextsetmodel_text2000_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='companyname_position',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
