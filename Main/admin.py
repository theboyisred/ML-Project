from django.contrib import admin
from .models import Job, AptitudeQuestion, PersonalityQuestion, Result
from django.utils.html import format_html

# Custom admin configuration for the Result model


class ResultAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = ("username", "role", "experience",
                    "years_of_experience", "display_image", "aptitude_test_result", "personality_type", "rank_score")
    # Set the specified fields as readonly in the admin view
    readonly_fields = ("username", "role", "experience",
                       "aptitude_test_result", "personality_type")

    # Function to calculate and display the total years of experience
    def years_of_experience(self, obj):
        # Load the JSON-formatted experience data from the model
        exp_dict: dict = obj.experience
        # Sum the years of experience
        exp = sum(map(lambda _: int(_), exp_dict.values()))
        return exp

    # Set a user-friendly name for the calculated field in the admin view
    years_of_experience.short_description = "Years of Experience"

    # Define a method to display the image as a link
    def display_image(self, obj):
        image_url = r"/media/B5.jpeg"
        return format_html('''<a href="{}"><img src="{}" style="max-height:100px; max-width:100px;" /></a>''', 
                           image_url, image_url)

    # Set a user-friendly name for the image link column
    display_image.short_description = "Personality Image"

    list_display_links = ("display_image",)
    ordering = ("-rank_score",)
    list_filter = ("role", )

# Register the models with the custom admin configurations
admin.site.register(Job)
admin.site.register(AptitudeQuestion)
admin.site.register(PersonalityQuestion)
admin.site.register(Result, ResultAdmin)
