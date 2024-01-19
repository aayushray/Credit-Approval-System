# Generated by Django 4.1 on 2024-01-18 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customer_current_debt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.IntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]