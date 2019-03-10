from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlihted = serializers.HyperlinkedIdentityField(view_name='snippets:snippet-highlight', format='html')
    class Meta:
        model = Snippet
        fields = ('id', 'owner', 'highlihted', 'title', 'code', 'linones', 'langauge', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippets:snippet-detail', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')