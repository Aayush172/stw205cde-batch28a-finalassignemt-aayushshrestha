# Generated by Django 3.2.6 on 2021-09-23 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.FileField(null=True, upload_to='static/upload'),
        ),
    ]
