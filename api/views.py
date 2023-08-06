from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import (
    Company,
    Job,
    WorkExperience,
    Workshop
)

from api.serializers import (
    CompanySerializer,
    JobSerializer,
    JobListSerializer,
    JwtSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    WorkExperienceSerializer,
    WorkshopSerializer
)

from api.pagination import JobPagination

# Create your views here.
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def public(request):
#     return JsonResponse({'message': 'Hello from a public endpoint!'})


class PublicView(APIView):
    """
    This view is for testing purposes only.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            '1': 'Never gonna give you up, never gonna let you down.',
            '2': 'Never gonna run around and desert you.',
            '3': 'Never gonna make you cry, never gonna say goodbye.',
            '4': 'Never gonna tell a lie and hurt you.'
        })


class RegisterUserView(generics.CreateAPIView):
    """
    This view is for registering a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    """
    This view is for retrieving and updating a user.
    User data is inferred from the provided username.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error retrieving user: {}".format(str(e))},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileSerializer(user.userprofile)
        return Response(serializer.data)

    def put(self, request, username):
        user = request.user,
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JwtView(TokenObtainPairView):
    """
    This view is for the user login endpoint
    """
    permission_classes = [AllowAny]
    serializer_class = JwtSerializer


class CompanyRegisterView(generics.ListCreateAPIView):
    """
    This view is for registering a new company.
    """
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    queryset = Company.objects.all()


class CompanyRetrieveView(generics.RetrieveAPIView):
    """
    This view is for retrieving a company based on the provided company ID
    as the query parameter.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            company = Company.objects.get(pk=id)
        except:
            return Response({"message": "Company with the specified id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobRegisterView(generics.CreateAPIView):
    """
    This view is for registering a new job.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        company_id = self.request.data.get('company_id')
        company = Company.objects.get(pk=company_id)
        serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobListView(generics.ListCreateAPIView):
    """
    This view is for retrieving a list of jobs, and for registering a new job.
    Pagination is applied to reduce the amount of data returned.
    TODO: Implement filtering classes
    """

    permission_classes = [IsAuthenticated]
    queryset = Job.objects.all()
    # pagination_class = JobPagination # Disable pagination for now

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'company__name': ["in"],
        'job_type': ["in"],
        'experience': ["in"],
    }

    def get_serializer_class(self):
        if (self.request.method == 'POST'):
            return JobSerializer
        elif self.request.method == 'GET':
            return JobListSerializer
        else:
            return JobSerializer

    def perform_create(self, serializer):
        company_id = self.request.data.get('company_id')
        company = Company.objects.get(pk=company_id)
        serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetailView(generics.RetrieveAPIView):
    """
    This view is for retrieving a job based on the provided job ID.
    Provides more detail than the above JobListView, as this view also returns
    the details on the qualifications and the responsibilities of the job.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get(self, request, id):
        try:
            job = Job.objects.get(pk=id)
        except:
            return Response({"message": "Job with the specified id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveJobView(APIView):
    """
    This view is for saving a job to the user's saved jobs list, as well as
    unsaving a job from the user's saved jobs list.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            id = request.data.get('job_id')
            job = Job.objects.get(pk=id)
            user = request.user
            if request.data.get("save") == False:
                user.userprofile.saved_jobs.remove(job)
                return Response({"message": "Job removed from saved jobs"})
            else:
                user.userprofile.saved_jobs.add(job)
                return Response({"message": "Job saved successfully"}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"message": "Job with the specified id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error saving job: {}".format(str(e))}, status=status.HTTP_400_BAD_REQUEST)


class WorkExperienceRegisterView(generics.ListCreateAPIView):
    """
    This view is for registering a new work experience.
    """
    serializer_class = WorkExperienceSerializer
    permission_classes = [AllowAny]
    queryset = WorkExperience.objects.all()


class WorkExperienceRetrieveView(generics.RetrieveAPIView):
    """
    This view is for retrieving a work experience based on the provided work experience ID
    as the query parameter.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            work_experience = WorkExperience.objects.get(pk=id)
        except:
            return Response({"message:": "Work Experience with the specified id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkExperienceSerializer(work_experience)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveWorkExperienceView(APIView):
    """
    This view is for saving a work experience to the user's saved work experience list, as well
    as unsaving a work experience from the user's saved work experience list.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            id = request.data.get('work_experience_id')
            work_experience = WorkExperience.objects.get(pk=id)
            user = request.user
            if request.data.get("save") == False:
                user.userprofile.saved_work_experiences.remove(work_experience)
                return Response({"message": "Work experience removed from saved work experiences"})
            else:
                user.userprofile.saved_work_experiences.add(work_experience)
                return Response({"message": "Work experience saved successfully"}, status=status.HTTP_200_OK)
        except WorkExperience.DoesNotExist:
            return Response({"message": "Work experience with the specified id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error saving work experience: {}".format(str(e))}, status=status.HTTP_400_BAD_REQUEST)


""" WORKSHOP VIEWS
"""


class WorkshopRegisterView(generics.ListCreateAPIView):
    """
    This view is for registering a new job.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'organizer__name': ["in"],
        'location': ["in"],
    }

    def perform_create(self, serializer):
        company_id = self.request.data.get('company_id')
        company = Company.objects.get(pk=company_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WorkshopRetrieveView(generics.RetrieveAPIView):
    """
    This view is for retrieving a workshop based on the provided workshop ID
    as the query parameter.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            workshop = Workshop.objects.get(pk=id)
        except:
            return Response({"message:": "Workshop with the specified id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkshopSerializer(workshop)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveWorkshopView(APIView):
    """
    This view is for saving a workshop to the user's saved workshops list, as well
    as unsaving a workshop from the user's saved workshops list.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            id = request.data.get('workshop_id')
            workshop = Workshop.objects.get(pk=id)
            user = request.user
            if request.data.get("save") == False:
                if workshop in user.userprofile.saved_workshops.all():
                    user.userprofile.saved_workshops.remove(workshop)
                    workshop.saves -= 1
                    workshop.save()
                    return Response({"message": "Workshop removed from saved workshops"})
                else:
                    return Response({"message": "Workshop not in saved workshops"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if workshop in user.userprofile.saved_workshops.all():
                    return Response({"message": "Workshop already in saved workshops"}, status=status.HTTP_400_BAD_REQUEST)
                user.userprofile.saved_workshops.add(workshop)
                workshop.saves += 1
                workshop.save()
                return Response({"message": "Workshop saved successfully"}, status=status.HTTP_200_OK)
        except Workshop.DoesNotExist:
            return Response({"message": "Workshop with the specified id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error saving workshop: {}".format(str(e))}, status=status.HTTP_400_BAD_REQUEST)


""" NEWCOMERS (FIX LATER)
"""

class RetrieveSavedJobsView(generics.ListAPIView):
    """
    This view is for retrieving the user's saved jobs.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = JobListSerializer

    def get_queryset(self):
        username = self.kwargs['username']  # Extract username from URL
        user = User.objects.get(username=username)
        return user.userprofile.saved_jobs.all()

class RetrievedSavedWorkshopsView(generics.ListAPIView):
    """
    This view is for retrieving the user's saved workshops.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WorkshopSerializer

    def get_queryset(self):
        username = self.kwargs['username']  # Extract username from URL
        user = User.objects.get(username=username)
        return user.userprofile.saved_workshops.all()
