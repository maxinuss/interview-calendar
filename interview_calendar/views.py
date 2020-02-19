import sys
from pprint import pprint
import math
from itertools import zip_longest

import numpy as np
from django.db.models.functions import datetime

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Interviewer, Candidate, CandidateSlot, InterviewerSlot, Interview
from rest_framework import viewsets, status
from .serializers import InterviewerSerializer, CandidateSerializer,\
    CandidateSlotSerializer, InterviewSerializer, InterviewerSlotSerializer

ERROR_NO_CANDIDATES = {"error": 'The is no candidates ready to talk now'}
ERROR_NO_INTERVIEWERS = {"error": 'The is no interviewers ready to talk now'}


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

    @action(detail=False, )
    def call(self, request):
        candidate_slots = get_available_candidate_slots()
        if len(candidate_slots) == 0:
            return Response(ERROR_NO_CANDIDATES, status=status.HTTP_404_NOT_FOUND)

        interviewer_slots = get_available_interviewer_slots()
        if len(interviewer_slots) == 0:
            return Response(ERROR_NO_INTERVIEWERS, status=status.HTTP_404_NOT_FOUND)

        interviewers_batch = get_interviewers_batch(interviewer_slots, candidate_slots)
        created_interviews = create_interviews(candidate_slots, interviewers_batch)

        return Response(created_interviews)

    @action(detail=False, url_path='call/candidates/(?P<candidate_pk>[^/.]+)')
    def call_with_candidate(self, request, candidate_pk):
        pass

    @action(detail=False, url_path='call/interviewers/(?P<interviewers_pk>[^/.]+)')
    def call_with_interviewer(self, request, interviewers_pk):
        pass


def create_interviews(candidate_slots, interviewers_batch):
    created_interviews = []
    today = datetime.datetime.today()

    for idx, val in enumerate(candidate_slots):
        candidate = val.candidate

        interview = Interview()
        interview.create(
            candidate=candidate,
            start_date=today,
            end_date=val.end_date,
            interviewers=interviewers_batch[idx]
        )
        created_interviews.append(InterviewSerializer(interview).data)

    return created_interviews


def get_available_candidate_slots():
    response = []
    today = datetime.datetime.today()
    return CandidateSlot.objects.filter(start_date__lte=today).filter(end_date__gte=today)


def get_available_interviewer_slots():
    response = []
    today = datetime.datetime.today()
    return InterviewerSlot.objects.filter(start_date__lte=today).filter(end_date__gte=today)


def get_interviewers_batch(interviewer_slots, candidate_slots):
    elements = []
    for interviewer_slot in interviewer_slots:
        elements.append(InterviewerSlotSerializer(interviewer_slot).data)

    return np.array_split(elements, len(candidate_slots))
