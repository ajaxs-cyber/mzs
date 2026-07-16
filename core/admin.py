from django.contrib import admin
from django.db.models import Count, Avg
from .models import Case, Message, SurveyResponse, PageVisit, UserProfile, ExperimentMetric


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'name', 'disease', 'created_at']
    list_display_links = ['title']
    list_editable = ['order']
    search_fields = ['title', 'name', 'disease']
    list_per_page = 20
    fieldsets = (
        ('基本信息', {'fields': ('title', 'name', 'disease')}),
        ('故事内容', {'fields': ('story', 'result')}),
        ('其他', {'fields': ('image', 'order')}),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['username', 'content_preview', 'is_approved', 'created_at']
    list_editable = ['is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['username', 'content']
    list_per_page = 30
    actions = ['approve_messages', 'unapprove_messages']

    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = '内容预览'

    def approve_messages(self, request, queryset):
        queryset.update(is_approved=True)
    approve_messages.short_description = '通过选中留言'

    def unapprove_messages(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_messages.short_description = '隐藏选中留言'


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'q1_score', 'q2_score', 'q3_score', 'q4_score', 'q5_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['q5']
    list_per_page = 30

    def q1_score(self, obj): return self._star(obj.q1)
    def q2_score(self, obj): return self._star(obj.q2)
    def q3_score(self, obj): return self._star(obj.q3)
    def q4_score(self, obj): return self._star(obj.q4)
    q1_score.short_description = 'Q1 继续了解'
    q2_score.short_description = 'Q2 音乐公益'
    q3_score.short_description = 'Q3 了解平台'
    q4_score.short_description = 'Q4 参与活动'

    def q5_preview(self, obj):
        return obj.q5[:30] + ('...' if len(obj.q5) > 30 else '') if obj.q5 else '-'
    q5_preview.short_description = '留言'

    @staticmethod
    def _star(val):
        return '★' * val + '☆' * (5 - val)


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['session_short', 'page', 'scroll_bar', 'duration_display', 'timestamp']
    list_filter = ['page', 'timestamp']
    list_per_page = 30

    def session_short(self, obj):
        return obj.session_id[:16] + '...'
    session_short.short_description = '会话ID'

    def scroll_bar(self, obj):
        pct = min(obj.scroll_percentage, 100)
        return f"{pct}%"
    scroll_bar.short_description = '滑动率'

    def duration_display(self, obj):
        s = obj.duration_seconds
        if s < 60:
            return f'{s}秒'
        m, sec = divmod(s, 60)
        return f'{m}分{sec}秒'
    duration_display.short_description = '停留时长'


@admin.register(ExperimentMetric)
class ExperimentMetricAdmin(admin.ModelAdmin):
    list_display = ['order', 'metric_name', 'value_a', 'value_b']
    list_display_links = ['metric_name']
    list_editable = ['order', 'value_a', 'value_b']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'email_verified', 'created_at']
    list_filter = ['email_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_per_page = 30
