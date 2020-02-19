""" This module contains models """
import sys
from pprint import pprint

from django.db import models


class Person(models.Model):
    """ This class set Person attributes """
    class Meta:
        """ This class set Abstract & unique_together attributes """
        abstract = True
        unique_together = ['name', 'last_name', ]

    name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=100)


class Interviewer(Person):
    """ This class set Interviewer attributes inherit from Person """


class Candidate(Person):
    """ This class set Candidate attributes inherit from Person """


class Interview(models.Model):
    """ This class set Interview attributes """
    class Meta:
        """ This class set Abstract & unique_together attributes """
        abstract = False
        unique_together = ['candidate', 'start_date', 'end_date', ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def create(self, candidate, start_date, end_date, interviewers):
        """
        Create an interview and interviewers relations.

        :param candidate:
        :type candidate:
        :param start_date:
        :type start_date:
        :param end_date:
        :type end_date:
        :param interviewers:
        :type interviewers:
        :return:
        :rtype:
        """
        self.candidate = candidate
        self.start_date = start_date
        self.end_date = end_date
        self.save()

        if len(interviewers) > 0:
            for interviewer in interviewers:
                interview_interviewer = InterviewInterviewer()
                interview_interviewer.create(interviewer=interviewer, interview=self)


class InterviewInterviewer(models.Model):
    """ This class set Interviewers relations with Interviews """
    class Meta:
        """ This class set Abstract & unique_together attributes """
        abstract = False
        unique_together = ['interview', 'interviewer', ]

    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
    )
    interviewer = models.ForeignKey(
        Interviewer,
        on_delete=models.CASCADE,
    )

    def create(self, interviewer, interview):
        """
        Create interviewers in an interview

        :param interviewer:
        :type interviewer:
        :param interview:
        :type interview:
        :return:
        :rtype:
        """
        self.interview = interview
        self.interviewer_id = interviewer['interviewer']
        self.save()


class Slot(models.Model):
    """ This class set Slot attributes """
    class Meta:  # pylint: disable=too-few-public-methods
        """ This class set Abstract attribute """
        abstract = True

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class InterviewerSlot(Slot):
    """ This class set Interviewer Slot attributes inherit from Slot """
    class Meta:
        """ This class set Abstract & unique_together attributes """
        abstract = False
        unique_together = ['start_date', 'end_date', 'interviewer', ]

    interviewer = models.ForeignKey(
        Interviewer,
        on_delete=models.CASCADE,
    )


class CandidateSlot(Slot):
    """ This class set Candidate Slot attributes inherit from Slot """
    class Meta:
        """ This class set Abstract & unique_together attributes """
        abstract = False
        unique_together = ['start_date', 'end_date', 'candidate', ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
    )
