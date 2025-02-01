from rest_framework import serializers
from apps.post.models import PostsModel, PostsPhotos

class PostsPhotosSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PostsPhotos
        fields = ['image']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class PostSerializer(serializers.ModelSerializer):
    photos = PostsPhotosSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='total_likes', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PostsModel
        fields = ['id', 'user_name', 'content', 'create_at', 'like_count', 'photos']
