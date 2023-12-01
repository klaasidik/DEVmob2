# Generated by Django 4.2.7 on 2023-11-28 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activityTracker', '0002_user_datedenaissance_user_motdepasse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idActivity', models.IntegerField(auto_created=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activityTracker.user')),
            ],
        ),
    ]
