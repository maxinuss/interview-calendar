import sys
from pprint import pprint

import numpy as np
from django.db import IntegrityError
from django.db.models.functions import datetime
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Interviewer, Candidate, CandidateSlot, InterviewerSlot, Interview
from rest_framework import viewsets, status
from .serializers import InterviewerSerializer, CandidateSerializer,\
    CandidateSlotSerializer, InterviewSerializer, InterviewerSlotSerializer

ERROR_CANDIDATE_NOT_EXISTS = {"error": 'This candidate does not exists'}
ERROR_INTERVIEWER_NOT_EXISTS = {"error": 'This interviewer does not exists'}
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
        """
        When this endpoint is called will check available candidates & interviewers
        and generate interviews

        :param request:
        :type request:
        :return:
        :rtype:
        """
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
        """
        When this endpoint is called will check available interviewers for a given candidate
        and generate interviews

        :param request:
        :type request:
        :param candidate_pk:
        :type candidate_pk:
        :return:
        :rtype:
        """
        try:
            candidate = Candidate.objects.get(pk=candidate_pk)
        except ObjectDoesNotExist:
            return Response(ERROR_CANDIDATE_NOT_EXISTS, status=status.HTTP_404_NOT_FOUND)

        candidate_slots = get_available_specific_candidate_slots(candidate)
        total_candidate_slots = get_available_candidate_slots()
        if len(candidate_slots) == 0:
            return Response(ERROR_NO_CANDIDATES, status=status.HTTP_404_NOT_FOUND)

        interviewer_slots = get_available_interviewer_slots()
        if len(interviewer_slots) == 0:
            return Response(ERROR_NO_INTERVIEWERS, status=status.HTTP_404_NOT_FOUND)

        interviewers_batch = get_interviewers_batch(interviewer_slots, total_candidate_slots)
        created_interviews = create_interviews(candidate_slots, interviewers_batch)

        return Response(created_interviews)

    @action(detail=False, url_path='call/interviewers/(?P<interviewers_pk>[^/.]+)')
    def call_with_interviewer(self, request, interviewers_pk):
        """
        When this endpoint is called will check available candidate for a given interviewer(s)
        and generate interviews

        :param request:
        :type request:
        :param interviewers_pk:
        :type interviewers_pk:
        :return:
        :rtype:
        """
        ids = interviewers_pk.split(",")
        interviewers = Interviewer.objects.filter(pk__in=ids)
        if len(interviewers) == 0 or len(interviewers) != len(ids):
            return Response(ERROR_INTERVIEWER_NOT_EXISTS, status=status.HTTP_404_NOT_FOUND)

        candidate_slots = get_available_candidate_slots(limit=1)
        if len(candidate_slots) == 0:
            return Response(ERROR_NO_CANDIDATES, status=status.HTTP_404_NOT_FOUND)

        interviewer_slots = get_available_specific_interviewer_slots(interviewers)
        if len(interviewer_slots) == 0:
            return Response(ERROR_NO_INTERVIEWERS, status=status.HTTP_404_NOT_FOUND)

        elements = []
        for interviewer_slot in interviewer_slots:
            elements.append(InterviewerSlotSerializer(interviewer_slot).data)

        interviewers_batch = [elements]
        created_interviews = create_interviews(candidate_slots, interviewers_batch)

        return Response(created_interviews)


def create_interviews(candidate_slots, interviewers_batch):
    """
    Create and return interviews

    :param candidate_slots:
    :type candidate_slots:
    :param interviewers_batch:
    :type interviewers_batch:
    :return:
    :rtype:
    """

    created_interviews = []
    today = datetime.datetime.today()

    try:
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
    except IntegrityError as e:
        return {"error": str(e)}


def get_available_candidate_slots(limit=None):
    """
    Get available candidate slots

    :return:
    :rtype:
    """
    today = datetime.datetime.today()
    return CandidateSlot.objects\
        .filter(start_date__lte=today)\
        .filter(end_date__gte=today)[:limit]


def get_available_specific_candidate_slots(candidate):
    """
    Get available slots for an specific candidate

    :return:
    :rtype:
    """
    today = datetime.datetime.today()
    return CandidateSlot.objects.filter(start_date__lte=today).filter(end_date__gte=today).filter(candidate=candidate)


def get_available_specific_interviewer_slots(interviewers):
    """
    Get available slots for an specific interviewer(s)

    :return:
    :rtype:
    """
    today = datetime.datetime.today()
    return InterviewerSlot.objects\
        .filter(start_date__lte=today)\
        .filter(end_date__gte=today)\
        .filter(interviewer__in=interviewers)


def get_available_interviewer_slots():
    """
    Get available interviewer slots

    :return:
    :rtype:
    """
    today = datetime.datetime.today()
    return InterviewerSlot.objects.filter(start_date__lte=today).filter(end_date__gte=today)


def get_interviewers_batch(interviewer_slots, candidate_slots):
    """
    Get batch of interviewers distributed evenly across candidates

    :param interviewer_slots:
    :type interviewer_slots:
    :param candidate_slots:
    :type candidate_slots:
    :return:
    :rtype:
    """
    elements = []
    for interviewer_slot in interviewer_slots:
        elements.append(InterviewerSlotSerializer(interviewer_slot).data)

    return np.array_split(elements, len(candidate_slots))
