# Generated by Django 2.1.2 on 2018-11-01 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminWorkspace', '0004_auto_20181018_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='catagory',
            name='color',
            field=models.CharField(default=1, max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catagory',
            name='image',
            field=models.FileField(default=None, null=True, upload_to=''),
        ),
    ]
