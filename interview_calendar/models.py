""" This module contains models """
from django.db import models


class Person(models.Model):
    """ This class set Person attributes """
    class Meta:  # pylint: disable=too-few-public-methods
        """ This class set Abstract attribute """
        abstract = True

    name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=100)


class Interviewer(Person):
    """ This class set Interviewer attributes inherit from Person """


class Candidate(Person):
    """ This class set Candidate attributes inherit from Person """


class Interview(models.Model):
    """ This class set Interview attributes """

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class InterviewInterviewer(models.Model):
    """ This class set Interviewers relations with Interviews """

    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
    )
    interviewer = models.ForeignKey(
        Interviewer,
        on_delete=models.CASCADE,
    )


class Slot(models.Model):
    """ This class set Slot attributes """
    class Meta:  # pylint: disable=too-few-public-methods
        """ This class set Abstract attribute """
        abstract = True

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class InterviewerSlot(Slot):
    """ This class set Interviewer Slot attributes inherit from Slot """

    interviewer = models.ForeignKey(
        Interviewer,
        on_delete=models.CASCADE,
    )


class CandidateSlot(Slot):
    """ This class set Candidate Slot attributes inherit from Slot """

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
    )
