# Generated by Django 5.0.4 on 2024-06-08 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_match_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='player1_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='match',
            name='player1_url',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='match',
            name='player2_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='match',
            name='player2_url',
            field=models.CharField(max_length=300),
        ),
    ]