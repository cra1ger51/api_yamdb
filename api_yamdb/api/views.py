from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, Title
from .serializers import CommentSerializer, ReviewSerializer
from .permissions import CustomPermission
from django.db.models import Avg

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (CustomPermission, )
    

    def get_one_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def update_title_rating(self):
        title = self.get_one_title()
        new_rating = Review.objects.filter(title__exact=title.id).aggregate(Avg('score'))
        title.update(rating=new_rating)

    def get_queryset(self):
        title = self.get_one_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_one_title()
        author = self.request.user
        serializer.save(author=author, title=title)
        self.update_title_rating()

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        self.update_title_rating()

    def destroy(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        self.update_title_rating()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (CustomPermission, )

    def get_one_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Title, pk=review_id)
        return review

    def get_queryset(self):
        review = self.get_one_review()
        return review.comment.all()

    def perform_create(self, serializer):
        review = self.get_one_title()
        author = self.request.user
        serializer.save(author=author, review=review)