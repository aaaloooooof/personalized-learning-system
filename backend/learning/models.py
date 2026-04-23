import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UUIDEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Learner(UUIDEntity):
    class LearningStyle(models.TextChoices):
        VISUAL = "visual", "Visual"
        AUDITORY = "auditory", "Auditory"
        READING_WRITING = "reading_writing", "Reading/Writing"
        KINESTHETIC = "kinesthetic", "Kinesthetic"
        MIXED = "mixed", "Mixed"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="learner_profile",
    )
    learning_style = models.CharField(
        max_length=32,
        choices=LearningStyle.choices,
        default=LearningStyle.MIXED,
    )
    total_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]
        verbose_name = "Learner"
        verbose_name_plural = "Learners"

    def __str__(self):
        return f"{self.user.username} ({self.get_learning_style_display()})"


class LearningPath(UUIDEntity):
    class GenerationType(models.TextChoices):
        MANUAL = "manual", "Manual"
        AI_GENERATED = "ai_generated", "AI Generated"
        HYBRID = "hybrid", "Hybrid"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    generation_type = models.CharField(
        max_length=32,
        choices=GenerationType.choices,
        default=GenerationType.MANUAL,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Learning Path"
        verbose_name_plural = "Learning Paths"

    def __str__(self):
        return self.name


class KnowledgePoint(UUIDEntity):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        RETIRED = "retired", "Retired"

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    weight = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Relative importance of the knowledge point on a 0.0-1.0 scale.",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    prerequisite = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dependent_points",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Knowledge Point"
        verbose_name_plural = "Knowledge Points"

    def __str__(self):
        return self.name


class LearningContent(UUIDEntity):
    class Format(models.TextChoices):
        VIDEO = "video", "Video"
        ARTICLE = "article", "Article"
        QUIZ = "quiz", "Quiz"
        AUDIO = "audio", "Audio"
        INTERACTIVE = "interactive", "Interactive"

    knowledge_point = models.ForeignKey(
        KnowledgePoint,
        on_delete=models.PROTECT,
        related_name="learning_contents",
    )
    title = models.CharField(max_length=255)
    format = models.CharField(
        max_length=24,
        choices=Format.choices,
        default=Format.ARTICLE,
    )
    content_url = models.URLField(max_length=500)
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Estimated duration in minutes.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Learning Content"
        verbose_name_plural = "Learning Contents"
        constraints = [
            models.UniqueConstraint(
                fields=["knowledge_point", "title"],
                name="unique_content_title_per_knowledge_point",
            )
        ]

    def __str__(self):
        return f"{self.title} [{self.get_format_display()}]"


class PathNode(UUIDEntity):
    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="path_nodes",
    )
    knowledge_point = models.ForeignKey(
        KnowledgePoint,
        on_delete=models.PROTECT,
        related_name="path_nodes",
    )
    sort_order = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["learning_path__name", "sort_order"]
        verbose_name = "Path Node"
        verbose_name_plural = "Path Nodes"
        constraints = [
            models.UniqueConstraint(
                fields=["learning_path", "sort_order"],
                name="unique_path_node_order_per_path",
            ),
            models.UniqueConstraint(
                fields=["learning_path", "knowledge_point"],
                name="unique_knowledge_point_per_learning_path",
            ),
        ]

    def __str__(self):
        return f"{self.learning_path.name} #{self.sort_order} - {self.knowledge_point.name}"


class LearningAssessment(UUIDEntity):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"

    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="learning_assessments",
    )
    title = models.CharField(max_length=255)
    total_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["learning_path__name", "title"]
        verbose_name = "Learning Assessment"
        verbose_name_plural = "Learning Assessments"
        constraints = [
            models.UniqueConstraint(
                fields=["learning_path", "title"],
                name="unique_assessment_title_per_learning_path",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.learning_path.name})"


class AssessmentResult(UUIDEntity):
    learner = models.ForeignKey(
        Learner,
        on_delete=models.CASCADE,
        related_name="assessment_results",
    )
    assessment = models.ForeignKey(
        LearningAssessment,
        on_delete=models.CASCADE,
        related_name="assessment_results",
    )
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Assessment Result"
        verbose_name_plural = "Assessment Results"
        indexes = [
            models.Index(fields=["learner", "created_at"]),
            models.Index(fields=["assessment", "created_at"]),
        ]

    def __str__(self):
        return f"{self.learner.user.username} - {self.assessment.title}: {self.score}"


class LearningRecord(UUIDEntity):
    learner = models.ForeignKey(
        Learner,
        on_delete=models.CASCADE,
        related_name="learning_records",
    )
    learning_content = models.ForeignKey(
        LearningContent,
        on_delete=models.CASCADE,
        related_name="learning_records",
    )
    progress = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Learning Record"
        verbose_name_plural = "Learning Records"
        constraints = [
            models.UniqueConstraint(
                fields=["learner", "learning_content"],
                name="unique_learning_record_per_learner_and_content",
            )
        ]

    def __str__(self):
        return f"{self.learner.user.username} - {self.learning_content.title} ({self.progress}%)"
