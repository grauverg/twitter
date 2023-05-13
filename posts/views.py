from datetime import datetime, timedelta

from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from . import paginations
from .permissions import IsAuthorOrIsAuthenticated, IsAdminOrReadOnly
from .models import Reply, Tweet, Reaction, ReactionType, ReplyReaction
from .serializers import TweetSerializer, ReplySerializer, \
    ReactionSerializer, ReactionTypeSerializer, ReplyReactionSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrIsAuthenticated, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = LimitOffsetPagination
    # pagination_class = paginations.TweetNumberPagination
    search_fields = ['text', 'profile__user__username']
    ordering_fields = ['updated_at', 'profile__user_id']

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    # @action(methods=['GET'], url_path='reaction_url', detail=False)
    # def reaction(self, request, pk=None):
    #     return Response(data={'key': 'value'})
    @action(
        methods=['POST'],
        detail=True,
        serializer_class=ReactionSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def reaction(self, request, pk=None):
        serializer = ReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                profile=self.request.user.profile,
                tweet=self.get_object()
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @action(
        methods=['GET'],
        detail=False,
        serializer_class=TweetSerializer
            )
    def recent(self, request):
        queryset = Tweet.objects.filter(
            created_at__gte=datetime.now()-timedelta(days=5)
        )
        serializer = TweetSerializer(queryset, many=True)
        return Response(serializer.data)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthorOrIsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])

    def perform_create(self, serializer):
        tweet_id = self.kwargs['tweet_id']
        tweet = Tweet.objects.get(id=tweet_id)
        serializer.save(tweet=tweet)


class ReplyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrIsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])


class ReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrIsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = LimitOffsetPagination
    search_fields = ['text', 'profile__user__username']
    ordering_fields = ['updated_at']

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])


class ReactionTypeViewSet(viewsets.ModelViewSet):
    queryset = ReactionType.objects.all()
    serializer_class = ReactionTypeSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class ReplyReactionCreateAPIView(generics.CreateAPIView):
    queryset = ReplyReaction.objects.all()
    serializer_class = ReplyReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            reply=get_object_or_404(Reply, pk=self.kwargs['reply_id'])
        )


class ReactionCreateAPIView(generics.CreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            tweet_id=self.kwargs['tweet_id']
        )


# class ReactionCreateAPIView(generics.CreateAPIView):
#     queryset = Reaction.objects.all()
#     serializer_class = ReactionSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(
#             profile=self.request.user.profile,
#             # tweet=Tweet.objects.get(id=self.kwargs['tweet_id'])
#             tweet_id=self.kwargs['tweet_id']
#         )
