# Generated by Django 5.1.4 on 2025-01-15 23:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stress', '0004_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('min_percent', models.IntegerField()),
                ('max_percent', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='recommendation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='stress.recommendation'),
        ),
    ]
