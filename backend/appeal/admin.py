from django.contrib import admin
from .models import Appeal, AppealImage

class AppealImageInline(admin.TabularInline):
    model = AppealImage
    extra = 1

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('user__email', 'description')
    inlines = [AppealImageInline]

@admin.register(AppealImage)
class AppealImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'appeal', 'uploaded_at')
    list_filter = ('uploaded_at',)
