from rest_framework.decorators import api_view

from .models import Interviewer, Candidate, CandidateSlot, InterviewerSlot, Interview
from rest_framework import viewsets
from .serializers import InterviewerSerializer, CandidateSerializer,\
    CandidateSlotSerializer, InterviewSerializer, InterviewerSlotSerializer


class InterviewerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Interviewers to be viewed or added.
    """
    queryset = Interviewer.objects.all()
    serializer_class = InterviewerSerializer
    http_method_names = ['get', 'post']


class CandidateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Candidates to be viewed or added.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    http_method_names = ['get', 'post']


class CandidateSlotViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Candidates slots to be viewed or added.
    """
    queryset = CandidateSlot.objects.all()
    serializer_class = CandidateSlotSerializer
    http_method_names = ['get', 'post']


class InterviewerSlotViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Interviewers slots to be viewed or added.
    """
    queryset = InterviewerSlot.objects.all()
    serializer_class = InterviewerSlotSerializer
    http_method_names = ['get', 'post']


class InterviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Interviews to be viewed or added.
    """
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    http_method_names = ['get', 'post']
