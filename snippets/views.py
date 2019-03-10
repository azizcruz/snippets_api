from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from pdb import set_trace
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly



from django.http import Http404
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action

# Create your views here.

@csrf_exempt
def list_snippets(request):
        """
        List all code snippets, or create a new snippet.
        """
        # List all snippets.
        if request.method == 'GET':
                snippet = Snippet.objects.all()
                serializer = SnippetSerializer(snippet, many=True)
                return JsonResponse(serializer.data, safe=False)

        # Create snippets.
        elif request.method == 'POST':
                data = JSONParser().parse(request)
                serializer = SnippetSerializer(data=data)
                if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data, status=201)
                return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
        """
        Retrieve, update or delete a code snippet.
        """

        try:
                snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist as e:
                return JsonResponse({'message': 'Snippet not found' })

        # Fetch snippet data.
        if request.method == 'GET':
                set_trace()
                serializer = SnippetSerializer(snippet)
                return JsonResponse(serializer.data)

        # Edit snippet data.
        elif request.method == 'PUT':
                data = JSONParser().parse(request)
                serializer = SnippetSerializer(snippet, data=data)
                if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, status=400)

        # Delete snippet
        elif request.method == 'DELETE':
                snippet.delete()
                return HttpResponse(status=204)

######################################################
###### Digging More Into Django Rest Framework #######
######################################################

@api_view(['GET', 'POST'])
def view_list_snippets(request, format=None):
        """
        List all code snippets, or create a new snippet.
        """
        
        # List all snippets.
        if request.method == 'GET':
                snippets = Snippet.objects.all()
                serializer = SnippetSerializer(snippets, many=True)
                return Response(serializer.data)
        
        # Create snippet.
        elif request.method == 'POST':
                serializer = SnippetSerializer(data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def view_snippet_detail(request, pk, format=None):
        """
        Retrieve, update or delete a code snippet.
        """
        # Get snippet object.
        try:
                snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        # List snippet detail.
        if request.method == 'GET':
                serializer = SnippetSerializer(snippet)
                return Response(serializer.data)

        # Edit snippet detail.
        if request.method == 'PUT':
                serializer = SnippetSerializer(snippet, data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Delete snippet.
        if request.method == 'DELETE':
                snippet.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)





######################################################
###### Class Based Views API #########################
######################################################

class SnippetList(APIView):
        """
        List all snippets, or create a new snippet.
        """
        # List all snippets.
        def get(self, request, format=None):
                snippets = Snippet.objects.all()
                serializer = SnippetSerializer(snippets, many=True)
                return Response(serializer.data)

        # Created a snippet.
        def post(self, request, format=None):
                serializer = SnippetSerializer(data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
        """
        Retrieve, update or delete a snippet instance.
        """

        def get_object(self, pk):
                try:
                        return Snippet.objects.get(pk=pk)
                except Snippet.DoesNotExist:
                        raise Http404

        # Fetch a Snippet.
        def get(self, request, pk, format=None):
                snippet = self.get_object(pk)
                serializer = SnippetSerializer(snippet)
                return Response(serializer.data)

        # Edit a Snippet.
        def put(self, request, pk, format=None):
                snippet = self.get_object(pk)
                serializer = SnippetSerializer(snippet, data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Delete a Snippet.
        def delete(self, request, pk, format=None):
                snippet = self.get_object(pk)
                snippet.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


######################################################
###### Generic Class Based Views API #################
######################################################

class GenericSnippetList(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer

        # List all snippets.
        def get(self, request, *args, **kwargs):
                return self.list(request, *args, **kwargs)
        # Add a snippet.
        def post(self, request, *args, **kwargs):
                return self.create(request, *args, **kwargs)

class GenericSnippetDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
        
        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer

        # Fetch a snippet.
        def get(self, request, *args, **kwargs):
                return self.retrieve(request, *args, **kwargs)

        # Update a snippet.
        def put(self, request, *args, **kwargs):
                return self.update(request, *args, **kwargs)

        # Delete a snippet.
        def delete(self, request, *args, **kwargs):
                return self.destroy(request, *args, **kwargs)

class GenericSnippetHeighlight(generics.GenericAPIView):
        queryset = Snippet.objects.all()
        renderer_classes = (renderers.StaticHTMLRenderer,)

        def get(self, request, *args, **kwargs):
                snippet = self.get_object()
                return Response(snippet.highlihted)



######################################################
###### Concised Generic Class Based Views API ########
######################################################

class ConcisedGenericSnippetList(generics.ListCreateAPIView):
        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

        def perform_create(self, serializer):
                serializer.save(owner=self.request.user)

class ConcisedGenericSnippetDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

class ConcisedGenericUserList(generics.ListAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer

class ConcisedGenericUserDetail(generics.RetrieveAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer


######################################################
###### Relationship & Hyperlink ######################
######################################################

# from rest_framework import reverse

# @api_view(['GET'])
# def api_root(request, format=None):
#         return Response({
#                 'users': reverse('users-list', request=request, format=format),
#                 'snippets': reverse('snippet-list', request=request, format=format)
#         })

######################################################
###### Usning Viewsets ###############################
######################################################

class SnippetViewSet(viewsets.ModelViewSet):
        """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

        Additionally we also provide an extra `highlight` action.
        """

        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

        @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
        def highlight(self, request, *args, **kwargs):
                snippet = self.get_object()
                return Response(snippet.highlihted)

        def perform_create(self, serializer):
                serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
        """
        This viewset automatically provides `list` and `detail` actions.
        """
        queryset = User.objects.all()
        serializer_class = UserSerializer