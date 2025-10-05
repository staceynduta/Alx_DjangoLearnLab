from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Event, EventCategory
from .serializers import (
    EventListSerializer,
    EventDetailSerializer,
    EventCreateUpdateSerializer,
    EventCategorySerializer,
)
from .filters import EventFilter
from .permissions import IsOrganizerOrReadOnly


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(is_published=True).select_related('organizer', 'category')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'location']
    ordering = ['-event_date']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventCreateUpdateSerializer
        return EventListSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class UpcomingEventsView(generics.ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Event.objects.filter(
            is_published=True,
            event_date__gt=timezone.now(),
            status='upcoming'
        ).select_related('organizer', 'category')


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsOrganizerOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EventCreateUpdateSerializer
        return EventDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organizer', 'category')
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(is_published=True)


class CategoryListView(generics.ListAPIView):
    queryset = EventCategory.objects.filter(is_active=True)
    serializer_class = EventCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = EventCategory.objects.filter(is_active=True)
    serializer_class = EventCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        upcoming_events = Event.objects.filter(
            category=instance,
            is_published=True,
            event_date__gt=timezone.now()
        ).select_related('organizer')[:5]

        data = serializer.data
        data['upcoming_events'] = EventListSerializer(
            upcoming_events,
            many=True,
            context={'request': request}
        ).data

        return Response(data)

