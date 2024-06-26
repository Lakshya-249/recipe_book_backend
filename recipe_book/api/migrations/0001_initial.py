# Generated by Django 5.0.6 on 2024-06-21 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('Main_Dishes', 'Main_Dishes'), ('Dessert', 'Dessert'), ('Drinks', 'Drinks'), ('Side Dishes', 'Side Dishes'), ('Appatizers', 'Appatizers')], max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('chef_id', models.AutoField(primary_key=True, serialize=False)),
                ('chef_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=250, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=130, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('recipe_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('image', models.CharField(max_length=300)),
                ('ingrediants', models.TextField()),
                ('steps', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chef')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chef')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.recipe')),
            ],
        ),
    ]
