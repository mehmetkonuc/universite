from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.post.models import PostsModel
from .serializers import PostSerializer

class PostsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = PostsModel.objects.all().order_by('-create_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})  # Burada request'i context olarak geçiyoruz
        return Response(serializer.data)