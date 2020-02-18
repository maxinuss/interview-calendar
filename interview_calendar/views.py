from .models import Interviewer
from rest_framework import viewsets
from .serializers import InterviewerSerializer


class InterviewerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Interviewer's to be viewed or edited.
    """
    queryset = Interviewer.objects.all()
    serializer_class = InterviewerSerializer
