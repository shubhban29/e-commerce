import datetime
from django.db import models
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authen.models import User
from authen.serializers import UserSerializer
import time
from datetime import date
from rest_framework import generics, mixins
from rest_framework import filters
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from authen.serializers import RegistrationSerializer, LoginSerializer
from .renderers import UserJSONRenderer

def current_user_details(request):
    user = User.objects.get(email=request.user.email)
    return dict(
        user=user,
        user_id=user.id)

def attach_to_dict(data, current_info, model):
    if "id" not in data or data["id"] == 0 or data["id"] == "" or data["id"] is None:
        data["created_by"] = current_info["user_id"]
        data["modified_by"] = current_info["user_id"]
    else:
        data["modified_by"] = current_info["user_id"]

def attach_to_list(data, current_info, model):
    for val in data:
        attach_to_dict(val, current_info, model)

def attach_current_info(data, current_info, model):
    if isinstance(data, dict):
        attach_to_dict(data, current_info, model)
    elif isinstance(data, list):
        attach_to_list(data, current_info, model)

class ResourceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = User
    resource_serializer = UserSerializer
    matching_condition = 0

    def get(self, request, pk):
        api_info = current_user_details(request)
        print(api_info['user'])
        try:
            resource_item = self.model.objects.filter(created_by=api_info['user']).get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.resource_serializer(resource_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        api_info = current_user_details(request)
        attach_current_info(request.data, api_info, self.model)
        try:
            resource_item = self.model.objects.filter(created_by=api_info['user']).get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.resource_serializer(resource_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        api_info = current_user_details(request)
        attach_current_info(request.data, api_info, self.model)
        print(request.data,"check1")
        if pk == self.matching_condition:
            serializer = self.resource_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                resource_item = self.model.objects.filter(created_by=api_info['user']).get(pk=pk)
            except self.model.DoesNotExist:
                return Response({'message': 'The resource does not exist'},status=status.HTTP_404_NOT_FOUND)
            serializer = self.resource_serializer(resource_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        api_info = current_user_details(request)
        try:
            resource_item = self.model.objects.filter(created_by=api_info['user']).get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'},status=status.HTTP_404_NOT_FOUND)
        resource_item.delete()
        return Response({'message': 'The resource is deleted successfully!'})


class SetPagination(PageNumberPagination):

    page_size = 50
    page_size_query_param = 'count'

    def get_paginated_response(self, data):
        return Response(data, status=status.HTTP_200_OK)


class GetListView(generics.ListAPIView):
    model = User
    resource_serializer = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = SetPagination
    filter_backends = [filters.SearchFilter]
    filter_query = []
    filter_data = None
    search_fields = []
    _exclude = None
    search_term = None
    Q1 = Q
    special_filter = []

    def get_queryset(self, page):
        """
        queryset of the Get
        """
        if page == 'all':
            queryset = self.model.objects.all()
            for val in self.filter_query:
                queryset.filter(**val)
            if self.filter_data:
                queryset = queryset.filter(**self.filter_data)
            if self._exclude:
                queryset = queryset.exclude(**self._exclude)
            if self.search_term:
                queryset = self.get_search_results_own(
                    queryset, self.search_term)
        else:
            m = int(page)
            if m == 0 or m == 1:
                queryset = self.model.objects.all()
                for val in self.filter_query:
                    queryset.filter(**val)
                if self.filter_data:
                    queryset = queryset.filter(**self.filter_data)
                if self._exclude:
                    queryset = queryset.exclude(**self._exclude)
                if self.search_term:
                    queryset = self.get_search_results_own(
                        queryset, self.search_term)
                queryset = queryset[:50]
            else:
                n = (m-1)*50
                queryset = self.model.objects.all()[n:n+50]
                for val in self.filter_query:
                    queryset.filter(**val)
                if self.filter_data:
                    queryset = queryset.filter(**self.filter_data)
                if self._exclude:
                    queryset = queryset.exclude(**self._exclude)
                if self.search_term:
                    queryset = self.get_search_results_own(
                        queryset, self.search_term)
                queryset = queryset[n:n+50]
        return queryset

    def list(self, request, page, *args, **kwargs):
        self.search_term = None
        page_count = request.GET.get('page', None)
        dict1 = {}
        self._exclude = {}
        self._current_special_filter = {}
        api_info = current_user_details(request)
        for k, v in request.query_params.items():
            fieldValue = v
            try:
                fieldValue = int(v)
            except:
                pass
            if k in self.special_filter:
                self._current_special_filter[k] = fieldValue
                continue
            if k == "search":
                self.search_term = v
                continue
            elif k.endswith("__exclude"):
                self._exclude[k[:-9]] = fieldValue
                continue
            if k.endswith('__in'):
                fieldValue = request.query_params.getlist(k)
            if k.endswith('__date'):
                fieldValue = datetime.datetime.strptime(fieldValue, "%Y-%m-%d")
                dict1[k[:-6]] = fieldValue
                continue
            dict1[k] = fieldValue
        if(request.GET.get('page', None) is not None):
            del dict1['page']
        if(request.GET.get('count', None) is not None):
            del dict1['count']
        self.filter_data = dict1
        self.filter_data['created_by'] = api_info['user']
        queryset = self.get_queryset(page)
        serializer = self.resource_serializer(queryset, many=True)
        if page == 'all':
            length = len(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        page_detail = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page_detail)


    def get_search_results_own(self, queryset, search_term):
        if search_term == None:
            return queryset
        if len(search_term) == 0:
            return queryset
        search_queries = None
        for index, val in enumerate(self.search_fields):
            temp_field = val
            if not val.endswith("contains"):
                temp_field = "{0}__icontains".format(val)
            temp = dict()
            temp[temp_field] = search_term
            if index == 0:
                search_queries = self.Q1(**temp)
            else:
                search_queries |= self.Q1(**temp)
        if search_queries is not None:
            return queryset.filter(search_queries)
        return queryset


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)