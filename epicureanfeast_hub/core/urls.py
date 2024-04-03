# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    recipe_list,
    recipe_detail,
    public_recipe_books,
    user_recipe_books,
    login_view,
    logout_view,
    signup,
    add_to_recipe_book,
    remove_from_recipe_book,
    like_recipe_book,
    rate_recipe,
    add_recipe_comment,
    recipe_book_detail,
    like_recipe_comment,
    followers,
    following,
    user_profile,
    toggle_follow,
    IngredientDetailView,
    create_recipe_book,
    all_ingredients
    #CreateRecipeBookView

)



urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('public-recipe-books/', public_recipe_books, name='public_recipe_books'),


    path('profile/<str:username>/recipe-books/', user_recipe_books, name='user_recipe_books'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('recipe/<int:recipe_id>/add-to-recipe-book/', add_to_recipe_book, name='add_to_recipe_book'),
    path('create-recipe-book/', create_recipe_book, name='create_recipe_book'),

    path('recipe-book/<int:recipe_book_id>/remove/', remove_from_recipe_book, name='remove_from_recipe_book'),
    path('recipe-book/<int:recipe_book_id>/like/', like_recipe_book, name='like_recipe_book'),
    path('recipe-comment/<int:recipe_comment_id>/like/', like_recipe_comment, name='like_recipe_comment'),
    path('recipe/<int:recipe_id>/rate/', rate_recipe, name='rate_recipe'),
    path('recipe/<int:recipe_id>/comment/', add_recipe_comment, name='add_recipe_comment'),
    path('recipe-book/<int:recipe_book_id>/', recipe_book_detail, name='recipe_book_detail'),

    path('user/<str:username>/', user_profile, name='user_profile'),
    path('user/<str:username>/follow/', toggle_follow, name='toggle_follow'),
    path('followers/<str:username>/', followers, name='followers'),
    path('following/<str:username>/', following, name='following'),

    path('ingredient/<int:ingredient_id>/', IngredientDetailView.as_view(), name='ingredient_detail'),
    #path('create-recipe-book/', CreateRecipeBookView.as_view(), name='create_recipe_book'),
    # ... other URL patterns ...
    # Add other URLs as needed
    path('ingredients/', all_ingredients, name='all_ingredients'),

]



