from django.contrib import admin

from .models import (
    AssessmentResult,
    KnowledgePoint,
    Learner,
    LearningAssessment,
    LearningContent,
    LearningPath,
    LearningRecord,
    PathNode,
)


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "learning_style",
        "total_score",
        "created_at",
        "updated_at",
    )
    list_filter = ("learning_style", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    autocomplete_fields = ("user",)


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ("name", "generation_type", "status", "created_at")
    list_filter = ("generation_type", "status", "created_at")
    search_fields = ("name", "description")


@admin.register(KnowledgePoint)
class KnowledgePointAdmin(admin.ModelAdmin):
    list_display = ("name", "weight", "status", "prerequisite", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "prerequisite__name")
    autocomplete_fields = ("prerequisite",)


@admin.register(LearningContent)
class LearningContentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "knowledge_point",
        "format",
        "duration",
        "created_at",
    )
    list_filter = ("format", "created_at", "knowledge_point__status")
    search_fields = ("title", "content_url", "knowledge_point__name")
    autocomplete_fields = ("knowledge_point",)


@admin.register(PathNode)
class PathNodeAdmin(admin.ModelAdmin):
    list_display = ("learning_path", "knowledge_point", "sort_order", "created_at")
    list_filter = ("created_at", "learning_path__status", "knowledge_point__status")
    search_fields = ("learning_path__name", "knowledge_point__name")
    autocomplete_fields = ("learning_path", "knowledge_point")


@admin.register(LearningAssessment)
class LearningAssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "learning_path", "total_score", "status", "created_at")
    list_filter = ("status", "created_at", "learning_path__status")
    search_fields = ("title", "learning_path__name")
    autocomplete_fields = ("learning_path",)


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ("learner", "assessment", "score", "passed", "created_at")
    list_filter = ("passed", "created_at", "assessment__status", "learner__learning_style")
    search_fields = (
        "learner__user__username",
        "learner__user__email",
        "assessment__title",
        "assessment__learning_path__name",
    )
    autocomplete_fields = ("learner", "assessment")


@admin.register(LearningRecord)
class LearningRecordAdmin(admin.ModelAdmin):
    list_display = (
        "learner",
        "learning_content",
        "progress",
        "completed",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "completed",
        "created_at",
        "updated_at",
        "learning_content__format",
        "learner__learning_style",
    )
    search_fields = (
        "learner__user__username",
        "learner__user__email",
        "learning_content__title",
        "learning_content__knowledge_point__name",
    )
    autocomplete_fields = ("learner", "learning_content")
