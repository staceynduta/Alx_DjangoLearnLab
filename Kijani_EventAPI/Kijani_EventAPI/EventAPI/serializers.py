"""
Serializers for Event management
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
from .models import Event, EventCategory


User = get_user_model()


class OrganizerSerializer(serializers.ModelSerializer):
    """Minimal organizer serializer"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EventCategorySerializer(serializers.ModelSerializer):
    """Serializer for Event Categories"""

    event_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'event_count']
        read_only_fields = ['id', 'slug']


class EventListSerializer(serializers.ModelSerializer):
    """Serializer for listing events"""

    organizer = OrganizerSerializer(read_only=True)
    category = EventCategorySerializer(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'event_date', 'end_date',
            'location', 'organizer', 'category', 'capacity', 'current_attendees',
            'available_spots', 'price', 'is_free', 'status', 'image_url',
            'is_full', 'is_published', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'current_attendees']


class EventDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single event"""

    organizer = OrganizerSerializer(read_only=True)
    category = EventCategorySerializer(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    can_register = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'event_date', 'end_date',
            'location', 'latitude', 'longitude', 'organizer', 'category',
            'capacity', 'current_attendees', 'available_spots', 'price',
            'is_free', 'status', 'image_url', 'registration_deadline',
            'is_published', 'allow_waitlist', 'is_full', 'is_past',
            'is_upcoming', 'can_register', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'organizer', 'created_at', 'updated_at', 'current_attendees']

    def get_can_register(self, obj):
        """Check if registration is still possible"""
        return obj.can_register()


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating events"""

    category = serializers.PrimaryKeyRelatedField(
        queryset=EventCategory.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_date', 'end_date', 'location',
            'latitude', 'longitude', 'category', 'capacity', 'price',
            'is_free', 'image_url', 'registration_deadline', 'allow_waitlist'
        ]

    def validate_event_date(self, value):
        """Validate that event date is in the future"""
        if value < timezone.now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value

    def validate_end_date(self, value):
        """Validate that end date is after event date"""
        if value:
            event_date = self.initial_data.get('event_date')
            if event_date and value < timezone.datetime.fromisoformat(event_date.replace('Z', '+00:00')):
                raise serializers.ValidationError("End date must be after event date.")
        return value

    def validate_registration_deadline(self, value):
        """Validate that registration deadline is before event date"""
        if value:
            event_date = self.initial_data.get('event_date')
            if event_date and value > timezone.datetime.fromisoformat(event_date.replace('Z', '+00:00')):
                raise serializers.ValidationError("Registration deadline must be before event date.")
        return value

    def validate_capacity(self, value):
        """Validate capacity is positive"""
        if value < 1:
            raise serializers.ValidationError("Capacity must be at least 1.")
        return value

    def validate(self, attrs):
        """Cross-field validation"""
        if self.instance:
            new_capacity = attrs.get('capacity', self.instance.capacity)
            if new_capacity < self.instance.current_attendees:
                raise serializers.ValidationError({
                    'capacity': f'Cannot reduce capacity below current attendees ({self.instance.current_attendees}).'
                })

        price = attrs.get('price', 0)
        is_free = attrs.get('is_free', True)
        if not is_free and price == 0:
            raise serializers.ValidationError({
                'price': 'Paid events must have a price greater than 0.'
            })

        return attrs

    def create(self, validated_data):
        """Create event with organizer"""
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


