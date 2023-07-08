from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import (
    Company,
    Job
)

from api.serializers import (
    CompanySerializer,
    JobSerializer,
    JobListSerializer,
    JwtSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
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

    def put(self, request):
        user = request.user
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
    pagination_class = JobPagination

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
