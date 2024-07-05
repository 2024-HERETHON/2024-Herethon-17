# Generated by Django 5.0.6 on 2024-07-03 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0005_program_application_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('application_method', models.CharField(max_length=200)),
                ('planned_changes', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]