from django.contrib import admin
from .models import Ingredient, Recipe, RecipeBook, RecipeRating, RecipeComment, UserProfile, Follow
#from .services import FirebaseService  # Import your FirebaseService if not already imported
#from io import BytesIO
#import mimetypes
#import base64
#from google.cloud import storage

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeBook)
admin.site.register(UserProfile)
admin.site.register(RecipeRating)
admin.site.register(RecipeComment)
admin.site.register(Follow)


#class RecipeAdmin(admin.ModelAdmin):
#    def save_model(self, request, obj, form, change):
#        super().save_model(request, obj, form, change)
#
#        if obj.image:
#            try:
#                # Set up the Google Cloud Storage client
#                client = storage.Client()
#
#                # Get the default bucket
#                bucket = client.get_bucket("epicureanfeasthub.appspot.com")
#
#                # Create a blob with a unique name
#                blob = bucket.blob(f"recipe_images/{obj.id}_{obj.image.name}")
#
#                # Upload the image to Firebase Storage
#                blob.upload_from_file(obj.image.file, content_type=obj.image.content_type)
#
#                # Get the download URL and save it in the model
#                obj.image_url = blob.public_url
#                obj.save(update_fields=["image_url"])
#            except Exception as e:
#                print(f"Error during image upload: {e}")
#
#admin.site.register(Recipe, RecipeAdmin)