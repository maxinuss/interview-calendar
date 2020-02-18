from .models import Interviewer, Interview, Candidate, InterviewerSlot, CandidateSlot
from rest_framework import serializers


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = ['id', 'name', 'last_name']


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'last_name']


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'candidate', 'start_date', 'end_date']


class InterviewerSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewerSlot
        fields = ['id', 'interviewer', 'start_date', 'end_date']


class CandidateSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSlot
        fields = ['id', 'candidate', 'start_date', 'end_date']