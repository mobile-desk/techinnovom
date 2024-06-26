# Generated by Django 5.0.1 on 2024-01-20 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_alter_recipebook_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cooking_type",
            field=models.CharField(
                choices=[
                    ("baking", "Baking"),
                    ("grilling", "Grilling"),
                    ("sauteing", "Sauteing"),
                    ("roasting", "Roasting"),
                    ("slow_cooking", "Slow Cooking"),
                    ("steaming", "Steaming"),
                    ("boiling", "Boiling"),
                    ("frying", "Frying"),
                    ("pressure_cooking", "Pressure Cooking"),
                    ("raw_vegan", "Raw/Vegan"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="food_type",
            field=models.CharField(
                choices=[
                    ("desserts", "Desserts"),
                    ("main_courses", "Main Courses"),
                    ("appetizers", "Appetizers"),
                    ("salads", "Salads"),
                    ("soups", "Soups"),
                    ("breakfast_brunch", "Breakfast/Brunch"),
                    ("beverages", "Beverages"),
                    ("snacks", "Snacks"),
                    ("side_dishes", "Side Dishes"),
                    ("gluten_free_options", "Gluten-Free Options"),
                ],
                max_length=50,
            ),
        ),
    ]
