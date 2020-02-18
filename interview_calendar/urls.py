from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'interviewers', views.InterviewerViewSet)
router.register(r'candidates', views.CandidateViewSet)
router.register(r'candidate-slots', views.CandidateSlotViewSet)
router.register(r'interviewer-slots', views.InterviewerSlotViewSet)
router.register(r'interviews', views.InterviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
]