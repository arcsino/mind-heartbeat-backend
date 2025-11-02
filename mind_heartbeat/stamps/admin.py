from django.contrib import admin
from .models import Stamp, Feeling


@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    list_display = ("name", "score", "id")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", "id")
    ordering = ("-created_at",)


@admin.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "stamp__name", "id")
    search_fields = ("comment", "created_by__username", "stamp__name")
    readonly_fields = ("created_at", "updated_at", "id")
    ordering = ("-created_at",)
