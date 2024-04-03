from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
#from .firebase_service import FirebaseService
#from io import BytesIO
#import mimetypes
#from django.core.files.storage import default_storage
#from django.core.files.base import ContentFile
#import requests



class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients')
    cooking_time = models.PositiveIntegerField()


    COOKING_TYPE_CHOICES = [
        ('baking', 'Baking'),
        ('grilling', 'Grilling'),
        ('sauteing', 'Sauteing'),
        ('roasting', 'Roasting'),
        ('slow_cooking', 'Slow Cooking'),
        ('steaming', 'Steaming'),
        ('boiling', 'Boiling'),
        ('frying', 'Frying'),
        ('pressure_cooking', 'Pressure Cooking'),
        ('raw_vegan', 'Raw/Vegan'),
        # Add more choices as needed
    ]

    cooking_type = models.CharField(max_length=50, choices=COOKING_TYPE_CHOICES)

    FOOD_TYPE_CHOICES = [
        ('desserts', 'Desserts'),
        ('main_courses', 'Main Courses'),
        ('appetizers', 'Appetizers'),
        ('salads', 'Salads'),
        ('soups', 'Soups'),
        ('breakfast_brunch', 'Breakfast/Brunch'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('side_dishes', 'Side Dishes'),
        ('gluten_free_options', 'Gluten-Free Options'),
        # Add more choices as needed
    ]
    food_type = models.CharField(max_length=50, choices=FOOD_TYPE_CHOICES)

    instructions = models.TextField()

    image = models.ImageField(upload_to="recipe_images/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    comments = models.ManyToManyField(User, through='RecipeComment', related_name='commented_recipes')
    ratings = models.ManyToManyField(User, through='RecipeRating', related_name='rated_recipes')
    total_rating = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)


    def __str__(self):
        return self.title

#    def save(self, *args, **kwargs):
#        super().save(*args, **kwargs)
#
#        # Handle image upload and URL retrieval
#        if self.image:
#            image_data = self.image.file.read()
#            content_type, encoding = mimetypes.guess_type(self.image.name)
#
#            # Upload the image to Firebase Storage
#            response = default_storage.save(f"images/{self.image.name}", ContentFile(image_data))
#
#            # Get the download URL and save it in the model
#            self.image_url = default_storage.url(response)
#
#            super().save(update_fields=["image_url"])




class RecipeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.recipe)

class RecipeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    class Meta:
        # Ensure a user can rate a recipe only once
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_user_recipe_rating')
        ]

    def __str__(self):
        return str(self.user) + ' ' + str(self.recipe)



#class Comment(models.Model):
#    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    text = models.TextField()
#    created_at = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return self.recipe + ' ' + str(self.created_at)

class RecipeBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_books')
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    recipes = models.ManyToManyField(Recipe)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_recipe_books', blank=True)
    comments = models.ManyToManyField(RecipeComment, blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ' ' + str(self.user)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following_users', blank=True)
    # Add any other fields you want for the user profile

    def __str__(self):
        return f"Profile of {self.user.username}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)