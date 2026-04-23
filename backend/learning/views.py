from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

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
from .serializers import (
    AssessmentResultSerializer,
    KnowledgePointSerializer,
    LearnerSerializer,
    LearningAssessmentSerializer,
    LearningContentSerializer,
    LearningPathSerializer,
    LearningRecordSerializer,
    PathNodeSerializer,
)


class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.select_related("user").all()
    serializer_class = LearnerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__username"]
    ordering_fields = ["created_at", "updated_at", "total_score", "user__username"]
    ordering = ["user__username"]


class LearningPathViewSet(viewsets.ModelViewSet):
    queryset = LearningPath.objects.prefetch_related(
        "path_nodes__knowledge_point",
    ).all()
    serializer_class = LearningPathSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name", "status"]
    ordering = ["name"]


class KnowledgePointViewSet(viewsets.ModelViewSet):
    queryset = KnowledgePoint.objects.select_related("prerequisite").all()
    serializer_class = KnowledgePointSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name", "weight", "status"]
    ordering = ["name"]


class LearningContentViewSet(viewsets.ModelViewSet):
    queryset = LearningContent.objects.select_related("knowledge_point").all()
    serializer_class = LearningContentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["format", "knowledge_point", "knowledge_point__status"]
    search_fields = ["title", "knowledge_point__name"]
    ordering_fields = ["created_at", "title", "duration"]
    ordering = ["title"]


class PathNodeViewSet(viewsets.ModelViewSet):
    queryset = PathNode.objects.select_related("learning_path", "knowledge_point").all()
    serializer_class = PathNodeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["learning_path", "knowledge_point"]
    search_fields = ["learning_path__name", "knowledge_point__name"]
    ordering_fields = ["created_at", "sort_order", "learning_path__name"]
    ordering = ["learning_path__name", "sort_order"]


class LearningAssessmentViewSet(viewsets.ModelViewSet):
    queryset = LearningAssessment.objects.select_related("learning_path").all()
    serializer_class = LearningAssessmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "learning_path"]
    search_fields = ["title", "learning_path__name"]
    ordering_fields = ["created_at", "title", "total_score"]
    ordering = ["learning_path__name", "title"]


class AssessmentResultViewSet(viewsets.ModelViewSet):
    queryset = AssessmentResult.objects.select_related(
        "learner__user",
        "assessment",
        "assessment__learning_path",
    ).all()
    serializer_class = AssessmentResultSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["passed", "learner", "assessment"]
    search_fields = ["learner__user__username", "assessment__title"]
    ordering_fields = ["created_at", "score"]
    ordering = ["-created_at"]


class LearningRecordViewSet(viewsets.ModelViewSet):
    queryset = LearningRecord.objects.select_related(
        "learner__user",
        "learning_content",
        "learning_content__knowledge_point",
    ).all()
    serializer_class = LearningRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["completed", "learner", "learning_content"]
    search_fields = ["learner__user__username", "learning_content__title"]
    ordering_fields = ["created_at", "updated_at", "progress"]
    ordering = ["-updated_at"]
