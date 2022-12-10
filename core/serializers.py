from django.db.models import fields
from rest_framework import serializers
from .models import Joke, Reaction


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model =Joke
        fields = ['id','caption','photo','reaction']

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reaction
        fields=['reaction']