from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import JokeSerializer,ReactionSerializer
from .models import Joke,Reaction
from rest_framework import permissions
from .permissions import IsPostedBy
# Create your views here.
class JokesFetch(ListCreateAPIView):
    serializer_class = JokeSerializer
    queryset = Joke.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(posted_by=self.request.user)

    def get_queryset(self):
        return self.queryset.all()

class JokesDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = JokeSerializer
    queryset = Joke.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsPostedBy)
    lookup_field="id"

    def get_queryset(self):
        return self.queryset.all()


class ReactionFetch(ListCreateAPIView):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(posted_by=self.request.user)

    def get_queryset(self):
        return self.queryset.all()

