# Generated by Django 3.2 on 2022-02-06 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ('-date',), 'verbose_name': 'Expense', 'verbose_name_plural': 'Expenses'},
        ),
    ]
