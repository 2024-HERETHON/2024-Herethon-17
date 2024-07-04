# Generated by Django 5.0.6 on 2024-07-03 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0006_policy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='application_method',
        ),
        migrations.RemoveField(
            model_name='policy',
            name='content',
        ),
        migrations.RemoveField(
            model_name='policy',
            name='planned_changes',
        ),
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('application_method', models.TextField()),
                ('planned_changes', models.TextField()),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='benefits', to='program.policy')),
            ],
        ),
    ]