# Generated by Django 4.2.6 on 2023-11-02 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_useraccount_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
