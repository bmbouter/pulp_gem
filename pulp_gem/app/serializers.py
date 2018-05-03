from rest_framework import serializers

from pulpcore.plugin.serializers import ContentSerializer, RemoteSerializer, PublisherSerializer

from .models import GemContent, GemRemote, GemPublisher


class GemContentSerializer(ContentSerializer):
    name = serializers.CharField(
        help_text='Name of the gem'
    )
    version = serializers.CharField(
        help_text='Version of the gem'
    )

    class Meta:
        fields = tuple(set(ContentSerializer.Meta.fields) - {'artifacts'}) + ('name', 'version')
        model = GemContent


class GemRemoteSerializer(RemoteSerializer):
    class Meta:
        fields = RemoteSerializer.Meta.fields
        model = GemRemote


class GemPublisherSerializer(PublisherSerializer):
    class Meta:
        fields = PublisherSerializer.Meta.fields
        model = GemPublisher
