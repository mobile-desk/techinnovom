# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Recipe, RecipeBook, UserProfile, Ingredient, RecipeRating, RecipeComment, Follow
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db.models import Sum  # Correct import for the Sum aggregation
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
import random
from django.contrib import messages



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('recipe_list')  # Replace 'home' with your desired redirect URL
        else:
            # Handle invalid login credentials
            messages.error(request,  'Invalid login credentials')
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'registration/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address already exists. Please use a different one.')
            return render(request, 'registration/signup.html')

        if password1 != password2:
            # Handle password mismatch
            messages.error(request, 'Passwords do not match')
            return render(request, 'registration/signup.html')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Create a corresponding UserProfile object
        UserProfile.objects.create(user=user)

        login(request, user)
        return redirect('recipe_list')  # Replace 'home' with your desired redirect URL

    return render(request, 'registration/signup.html')



def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)


    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        rating_value = request.POST.get('rating')

        try:
            rating_value = int(rating_value)
        except ValueError:
            pass

        if not (1 <= rating_value <= 5):
            pass


        # Check if the user has already rated this recipe
        existing_rating = RecipeRating.objects.filter(user=request.user, recipe=recipe).first()

        if existing_rating:
            pass

        # If the user hasn't rated before, create a new rating

        else:
            # If the user hasn't rated before, create a new rating
            RecipeRating.objects.create(user=request.user, recipe=recipe, rating=rating_value)#
            # Update Recipe model's rating fields
            recipe.refresh_from_db()
            recipe_rating_sum = RecipeRating.objects.filter(recipe=recipe).aggregate(Avg('rating'))['rating__avg'] or 0
            recipe.rating_count = RecipeRating.objects.filter(recipe=recipe).count()
            recipe.average_rating = round(recipe_rating_sum, 2)
            recipe.save()

    return redirect('recipe_detail', recipe_id=recipe_id)

@login_required
def add_recipe_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    text = request.POST.get('comment_text')  # Assuming you have a form field with 'comment_text'

    if text:
        RecipeComment.objects.create(user=request.user, recipe=recipe, text=text)

    return redirect('recipe_detail', recipe_id=recipe_id)

@login_required
def public_recipe_books(request):
    # Get public recipe books
    public_books = RecipeBook.objects.filter(is_public=True)
    return render(request, 'public_recipe_books.html', {'public_books': public_books})

def recipe_list(request):
    query = request.GET.get('q')
    time_filter = request.GET.get('time')
    food_type_filter = request.GET.get('food_type')
    cooking_type_filter = request.GET.get('cooking_type')

    # Get a list of ingredients the user has in their fridge
    user_ingredients = request.GET.getlist('ingredients')
    all_ingredients = Ingredient.objects.all()

    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(instructions__icontains=query) |
            Q(ingredients__name__icontains=query)
        ).distinct()

    if time_filter:
        recipes = recipes.filter(cooking_time__lte=int(time_filter))

    if food_type_filter:
        recipes = recipes.filter(food_type=food_type_filter)

    if cooking_type_filter:
        recipes = recipes.filter(cooking_type=cooking_type_filter)

    # Filter recipes based on user's ingredients
    for ingredient_name in user_ingredients:
        recipes = recipes.filter(ingredients__name=ingredient_name)

    return render(request, 'recipe_list.html', {'recipes': recipes, 'all_ingredients': all_ingredients})

def user_recipe_books(request, username):
    user = get_object_or_404(User, username=username)
    recipe_books = RecipeBook.objects.filter(user=user)
    return render(request, 'user_recipe_books.html', {'user': user, 'recipe_books': recipe_books})

def recipe_book_detail(request, recipe_book_id):
    recipe_book = get_object_or_404(RecipeBook, pk=recipe_book_id)
    recipes = recipe_book.recipes.all()  # Assuming the related name is 'recipes'

    return render(request, 'recipe_book_detail.html', {'recipe_book': recipe_book, 'recipes': recipes})

@login_required
def add_to_recipe_book(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Get the user's recipe books
    user_recipe_books = RecipeBook.objects.filter(user=request.user)

    if request.method == 'POST':
        selected_recipe_book_id = request.POST.get('recipe_book')
        selected_recipe_book = get_object_or_404(RecipeBook, pk=selected_recipe_book_id)

        # Add the recipe to the selected recipe book
        selected_recipe_book.recipes.add(recipe)
        return redirect('user_recipe_books', username=request.user.username)

    return render(request, 'select_recipe_book.html', {'user_recipe_books': user_recipe_books, 'recipe': recipe})


def create_recipe_book(request):
    if request.method == 'POST':
        new_recipe_book_name = request.POST.get('new_recipe_book')

        # Check if a recipe book with the same name already exists
        if not RecipeBook.objects.filter(name=new_recipe_book_name, user=request.user).exists():
            # Create a new recipe book
            RecipeBook.objects.create(name=new_recipe_book_name, user=request.user)

    # Redirect to a page or view after creating the recipe book
    # Check for 'next' parameter in the query string
    next_url = request.GET.get('next', None)

    # If 'next' is not present, redirect to public_recipe_books
    if not next_url:
        return redirect('recipe_list')


    # Use Django's reverse function to get the URL for the 'next' parameter
    return redirect(next_url)




@login_required
def remove_from_recipe_book(request, recipe_book_id):
    recipe_book = get_object_or_404(RecipeBook, pk=recipe_book_id)
    recipe_id = request.POST.get('recipe_id')  # Assuming you have a form field with 'recipe_id'
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if recipe in recipe_book.recipes.all():
        recipe_book.recipes.remove(recipe)
        recipe_book.save()

    return redirect('user_recipe_books', username=request.user.username)

@login_required
def like_recipe_book(request, recipe_book_id):
    recipe_book = get_object_or_404(RecipeBook, pk=recipe_book_id)

    if request.user in recipe_book.likes.all():
        recipe_book.likes.remove(request.user)
    else:
        recipe_book.likes.add(request.user)

    recipe_book.save()

    # Check for 'next' parameter in the query string
    next_url = request.GET.get('next', None)

    # If 'next' is not present, redirect to public_recipe_books
    if not next_url:
        return redirect('public_recipe_books')


    # Use Django's reverse function to get the URL for the 'next' parameter
    return redirect(next_url)

@login_required
def like_recipe_comment(request, recipe_comment_id):
    recipe_comment = get_object_or_404(RecipeComment, pk=recipe_comment_id)

    if request.user in recipe_comment.likes.all():
        recipe_comment.likes.remove(request.user)
    else:
        recipe_comment.likes.add(request.user)

    recipe_comment.save()

    # Check for 'next' parameter in the query string
    next_url = request.GET.get('next', None)

    # If 'next' is not present, redirect to recipe_detail
    if not next_url:
        return redirect('recipe_detail', recipe_id=recipe_comment.recipe.id)

    # Use Django's reverse function to get the URL for the 'next' parameter
    return redirect(next_url)


def user_profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    followers = user_profile.followers.all()
    following = user_profile.user.following.all()
    recipe_books = user_profile.user.recipe_books.all()
    total_recipe_books = recipe_books.count()

    is_following = Follow.objects.filter(user=request.user, followed_user=user_profile.user).exists()

    context = {
        'user_profile': user_profile,
        'followers': followers,
        'following': following,
        'is_following': is_following,
        'recipe_books': recipe_books,
        'total_recipe_books': total_recipe_books,
    }

    return render(request, 'user_profile.html', context)

def toggle_follow(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if Follow.objects.filter(user=request.user, followed_user=user_profile.user).exists():
                # User is already following, unfollow
                Follow.objects.filter(user=request.user, followed_user=user_profile.user).delete()
            else:
                # User is not following, follow
                Follow.objects.create(user=request.user, followed_user=user_profile.user)

    return redirect('user_profile', username=username)



def followers(request, username):
    user_profile = UserProfile.objects.get(user__username=username)
    followers = user_profile.followers.all()
    return render(request, 'followers.html', {'followers': followers})

def following(request, username):
    user_profile = UserProfile.objects.get(user__username=username)
    following = user_profile.user.following.all()
    return render(request, 'following.html', {'following': following})



class IngredientDetailView(View):
    template_name = 'ingredient_detail.html'

    def get(self, request, ingredient_id):
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)

        # Get three random recipes that use the ingredient
        related_recipes = Recipe.objects.filter(ingredients=ingredient)
        random_recipes = random.sample(list(related_recipes), min(3, related_recipes.count()))

        return render(request, self.template_name, {'ingredient': ingredient, 'random_recipes': random_recipes})


def all_ingredients(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'all_ingredients.html', {'ingredients': ingredients})
