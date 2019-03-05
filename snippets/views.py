from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer
from pdb import set_trace
from rest_framework import status

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






