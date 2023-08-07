import jwt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from datetime import datetime
from django.http import JsonResponse
from .serializers import *

from .auth_decorator import authenticate_token, authenticate_admin


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):

        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found')

        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'role': user.role
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.data = ({
            'id': user.id,
            'name': user.name,
            'jwt': token,
            'email': email,
            'role': user.role
        })

        response.set_cookie(key='jwt', value=token, httponly=True, expires=payload['exp'])
        return response

class GetAllUsersForAdmin(APIView):
    @authenticate_token
    @authenticate_admin
    def get(self, request):

        userset = User.objects.filter(role="user")
        serializer = UserSerializer(userset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetUserView(APIView):
    @authenticate_token
    def get(self, request):

        # print(request.META.get('HTTP_AUTHORIZATION'))
        token = request.headers["Authorization"].split("Bearer ")[1]
        print('token is:  ', token)
        decoded_token = jwt.decode(token, key='secret', algorithms=['HS256'])
        user_id = decoded_token.get('id')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        res = serializer.data
        res["id"] = user_id
        return Response(res, status=status.HTTP_200_OK)

class ViewAdminPlans(APIView):
    @authenticate_token
    @authenticate_admin
    def get(self, request, user_id):
        planset = Plan.objects.filter(author__id=user_id)

        serializer = PlanSerializer(planset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddPlanView(APIView):
    @authenticate_token
    @authenticate_admin
    def post(self, request):

        serializer = PlanSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewDetailedPlanView(APIView):
    @authenticate_token
    def get(self, request, plan_id):
        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewPlanList(APIView):
    def get(self, request):
        planset = Plan.objects.all()
        serializer = PlanSerializer(planset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateDateView(APIView):
    @authenticate_token
    @authenticate_admin
    def put(self, request, plan_id):

        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlanSerializer(plan, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'date updated'}, status=status.HTTP_200_OK)

        return Response({'message': 'invalid dates'}, status=status.HTTP_400_BAD_REQUEST)

class DeletePlanView(APIView):
    @authenticate_token
    @authenticate_admin
    def delete(self, request, plan_id):
        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)

        plan.delete()
        return Response({'message': 'plan deleted successfully'}, status=status.HTTP_200_OK)

class RegisterPlanView(APIView):
    @authenticate_token
    def post(self, request, plan_id, user_id):

        # token = request.COOKIES.get('user_jwt')
        # if not token:
        #     raise AuthenticationFailed('user not logged in')

        # user_id = request.data.get('id')
        user = User.objects.get(pk=user_id)

        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)

        if PlanWithUserRegistration.objects.filter(user=user, plan=plan).exists():
            return Response({'error': 'user already registered'}, status=status.HTTP_400_BAD_REQUEST)

        PlanWithUserRegistration.objects.create(user=user, plan=plan)
        return Response({'message': 'user registered successfully'}, status=status.HTTP_201_CREATED)

class CheckPlanRegistrationStatus(APIView):
    @authenticate_token
    def get(self, request, plan_id, user_id):

        # user_id = request.data.get('id')
        user = User.objects.get(pk=user_id)

        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'plan not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            registration = PlanWithUserRegistration.objects.get(user=user, plan=plan)
        except PlanWithUserRegistration.DoesNotExist:
            return Response({False}, status=status.HTTP_200_OK)

        return Response({True}, status=status.HTTP_200_OK)

class DeregisterPlanView(APIView):
    @authenticate_token
    def post(self, request, plan_id, user_id):

        # user_id = request.data.get('id')
        user = User.objects.get(pk=user_id)

        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            registration = PlanWithUserRegistration.objects.filter(user=user, plan=plan)
        except PlanWithUserRegistration.DoesNotExist:
            return Response({'error': 'no registration exists'}, status=status.HTTP_400_BAD_REQUEST)

        registration.delete()
        return Response({'message': 'deregistered successfully'}, status=status.HTTP_200_OK)

class ViewRegisteredPlans(APIView):
    @authenticate_token
    def get(self, request, user_id):

        registered_plans = Plan.objects.filter(participants__pk=user_id)
        serializer = PlanSerializer(registered_plans, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ViewRegisteredUsersForPlan(APIView):
    @authenticate_token
    @authenticate_admin
    def get(self, request, plan_id):
        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)

        registered_users = User.objects.filter(planwithuserregistration__plan=plan)
        serializer = UserSerializer(registered_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
