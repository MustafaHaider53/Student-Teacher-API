from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.models import User , Assingment , Submission , Grade

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "name" , "password", "role" , "is_admin"]
    list_filter = ["email"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_admin" , "role"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name" , "password", "role"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)


@admin.register(Assingment)
class AssingmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'illustration', 'created_by', 'assigned_to']



@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['solution' , 'assingment']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['assingment' , 'graded_by' , 'graded_to' , 'grades']
    


    



