from django.contrib import admin
from .models import Case, Message, SurveyResponse, PageVisit


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'disease', 'order', 'created_at']
    list_editable = ['order']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['username', 'content_short', 'is_approved', 'created_at']
    list_editable = ['is_approved']

    def content_short(self, obj):
        return obj.content[:40]


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'q1', 'q2', 'q3', 'q4', 'q5_short', 'created_at']

    def q5_short(self, obj):
        return obj.q5[:30]


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'page', 'scroll_percentage', 'duration_seconds', 'timestamp']
