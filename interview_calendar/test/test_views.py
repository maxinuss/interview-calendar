import json
from rest_framework import status
from rest_framework.test import APITestCase

class TestInterviewerViewSet(APITestCase):

    def test_add_interviewer(self):
        data = {"name": "Test", "last_name": "Case"}
        response = self.client.post("/interviewers/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_interviewer(self):
        response = self.client.get("/interviewers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCandidateViewSet(APITestCase):

    def test_add_candidate(self):
        data = {"name": "Test", "last_name": "Case"}
        response = self.client.post("/candidates/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_candidate(self):
        response = self.client.get("/candidates/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCandidateSlotViewSet(APITestCase):

    def test_get_candidate_slot(self):
        response = self.client.get("/candidate-slots/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestInterviewerSlotViewSet(APITestCase):

    def test_get_interviewer_slot(self):
        response = self.client.get("/interviewer-slots/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestInterviewViewSet(APITestCase):

    def test_get_interview(self):
        response = self.client.get("/interviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
