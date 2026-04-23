from rest_framework.routers import DefaultRouter

from .views import (
    AssessmentResultViewSet,
    KnowledgePointViewSet,
    LearnerViewSet,
    LearningAssessmentViewSet,
    LearningContentViewSet,
    LearningPathViewSet,
    LearningRecordViewSet,
    PathNodeViewSet,
)

router = DefaultRouter()
router.register("learners", LearnerViewSet, basename="learner")
router.register("learning-paths", LearningPathViewSet, basename="learningpath")
router.register("knowledge-points", KnowledgePointViewSet, basename="knowledgepoint")
router.register("learning-contents", LearningContentViewSet, basename="learningcontent")
router.register("path-nodes", PathNodeViewSet, basename="pathnode")
router.register("learning-assessments", LearningAssessmentViewSet, basename="learningassessment")
router.register("assessment-results", AssessmentResultViewSet, basename="assessmentresult")
router.register("learning-records", LearningRecordViewSet, basename="learningrecord")

urlpatterns = router.urls
