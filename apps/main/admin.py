from django.contrib import admin

from .models import (User,
                     PostModel,
                     LikeModel)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(PostModel, admin.ModelAdmin)
admin.site.register(LikeModel, admin.ModelAdmin)
