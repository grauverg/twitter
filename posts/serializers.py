from rest_framework import serializers
from django.db.utils import IntegrityError

from .models import Tweet, Reply,\
    ReactionType, Reaction, ReplyReaction


class TweetSerializer(serializers.ModelSerializer):
    reactions = serializers.ReadOnlyField(source='get_reactions')
    all_reactions = serializers.ReadOnlyField()

    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ['profile', ]


class ReplySerializer(serializers.ModelSerializer):
    reactions = serializers.ReadOnlyField(source='get_reactions')

    class Meta:
        model = Reply
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            new_reaction_type = validated_data.pop('reaction')
            instance = self.Meta.model.objects.get(**validated_data)
            instance.reaction = new_reaction_type
            instance.save()
            return instance


class ReplyReactionSerializer(ReactionSerializer):
    class Meta:
        model = ReplyReaction
        fields = '__all__'
        read_only_fields = ['profile', 'reply']


class ReactionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReactionType
        fields = '__all__'
        read_only_fields = ['profile', 'tweet', ]
