# Generated by Django 4.2.6 on 2023-11-02 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_excelfile_delete_uploadedexcelfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='website',
            field=models.CharField(choices=[('Sportybet', 'Sportybet'), ('Xbet', 'Xbet'), ('Betway', 'Betway')], max_length=20),
        ),
    ]
