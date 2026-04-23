from rest_framework import serializers

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


class LearnerSerializer(serializers.ModelSerializer):
    user_username = serializers.SlugRelatedField(
        source="user",
        slug_field="username",
        read_only=True,
    )
    user_email = serializers.SlugRelatedField(
        source="user",
        slug_field="email",
        read_only=True,
    )

    class Meta:
        model = Learner
        fields = [
            "id",
            "user",
            "user_username",
            "user_email",
            "learning_style",
            "total_score",
            "created_at",
            "updated_at",
        ]


class KnowledgePointSerializer(serializers.ModelSerializer):
    prerequisite_name = serializers.SlugRelatedField(
        source="prerequisite",
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = KnowledgePoint
        fields = [
            "id",
            "name",
            "description",
            "weight",
            "status",
            "prerequisite",
            "prerequisite_name",
            "created_at",
        ]


class PathNodeSerializer(serializers.ModelSerializer):
    learning_path_name = serializers.SlugRelatedField(
        source="learning_path",
        slug_field="name",
        read_only=True,
    )
    knowledge_point_name = serializers.SlugRelatedField(
        source="knowledge_point",
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = PathNode
        fields = [
            "id",
            "learning_path",
            "learning_path_name",
            "knowledge_point",
            "knowledge_point_name",
            "sort_order",
            "created_at",
        ]


class LearningPathSerializer(serializers.ModelSerializer):
    path_nodes = PathNodeSerializer(many=True, read_only=True)

    class Meta:
        model = LearningPath
        fields = [
            "id",
            "name",
            "description",
            "generation_type",
            "status",
            "created_at",
            "path_nodes",
        ]


class LearningContentSerializer(serializers.ModelSerializer):
    knowledge_point_name = serializers.SlugRelatedField(
        source="knowledge_point",
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = LearningContent
        fields = [
            "id",
            "knowledge_point",
            "knowledge_point_name",
            "title",
            "format",
            "content_url",
            "duration",
            "created_at",
        ]


class LearningAssessmentSerializer(serializers.ModelSerializer):
    learning_path_name = serializers.SlugRelatedField(
        source="learning_path",
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = LearningAssessment
        fields = [
            "id",
            "learning_path",
            "learning_path_name",
            "title",
            "total_score",
            "status",
            "created_at",
        ]


class AssessmentResultSerializer(serializers.ModelSerializer):
    learner_username = serializers.SlugRelatedField(
        source="learner.user",
        slug_field="username",
        read_only=True,
    )
    assessment_title = serializers.SlugRelatedField(
        source="assessment",
        slug_field="title",
        read_only=True,
    )

    class Meta:
        model = AssessmentResult
        fields = [
            "id",
            "learner",
            "learner_username",
            "assessment",
            "assessment_title",
            "score",
            "passed",
            "created_at",
        ]


class LearningRecordSerializer(serializers.ModelSerializer):
    learner_username = serializers.SlugRelatedField(
        source="learner.user",
        slug_field="username",
        read_only=True,
    )
    learning_content_title = serializers.SlugRelatedField(
        source="learning_content",
        slug_field="title",
        read_only=True,
    )

    class Meta:
        model = LearningRecord
        fields = [
            "id",
            "learner",
            "learner_username",
            "learning_content",
            "learning_content_title",
            "progress",
            "completed",
            "created_at",
            "updated_at",
        ]
