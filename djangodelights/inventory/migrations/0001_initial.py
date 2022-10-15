# Generated by Django 4.1.1 on 2022-10-08 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('quantity', models.FloatField(verbose_name='Quantity')),
                ('unit', models.CharField(choices=[('g', 'gram'), ('tbsp', 'tablespoon'), ('tsp', 'teaspoon'), ('l', 'liter'), ('cup', 'cup'), ('oz', 'ounces'), ('lbs', 'pound'), ('', '')], default='', max_length=10, verbose_name='Unit of Measure')),
                ('unit_price', models.FloatField(default=0.0, verbose_name='Unit Price')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Item Name')),
                ('price', models.FloatField(default=0.0, verbose_name='Price')),
                ('description', models.CharField(max_length=500, verbose_name='Item Description')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='RecipeRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0, verbose_name='Quantity')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ingredient', verbose_name='Ingredient')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.menuitem', verbose_name='Menu Item')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='DateTime')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.menuitem', verbose_name='Menu Item')),
            ],
            options={
                'ordering': ['menu_item'],
            },
        ),
    ]
