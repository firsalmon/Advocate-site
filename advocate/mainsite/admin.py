# mainsite/admin.py
from django.contrib import admin
from .models import Lead, Review, ThankfulLetter, Questions

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at", "is_processed")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "phone")
    list_editable = ("is_processed",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Данные клиента", {"fields": ("name", "phone", "message")}),
        ("Статус", {"fields": ("is_processed", "created_at")}),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "case_type", "year", "is_published", "created_at")
    list_filter = ("is_published", "year")
    search_fields = ("author", "text")
    list_editable = ("is_published",)
    fieldsets = (
        ("Основное", {"fields": ("author", "text")}),
        ("Детали", {"fields": ("case_type", "year", "is_published")}),
    )

@admin.register(ThankfulLetter)
class ThankfulLetterAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title",)
    list_editable = ("is_published",)
    fieldsets = (
        ("Контент", {"fields": ("title", "image", "link")}),
        ("Публикация", {"fields": ("is_published",)}),
    )

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("question", "priority", "is_published", "id")
    list_filter = ("priority", "is_published")
    search_fields = ("question", "answer")
    list_editable = ("priority", "is_published")
    ordering = ("-priority", "question", "is_published")
    fields = ('question', 'answer', 'priority', "is_published")

