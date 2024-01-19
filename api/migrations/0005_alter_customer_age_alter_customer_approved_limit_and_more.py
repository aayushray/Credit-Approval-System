# Generated by Django 4.1 on 2024-01-18 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_customer_loan_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='age',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='approved_limit',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='monthly_salary',
            field=models.IntegerField(),
        ),
    ]
