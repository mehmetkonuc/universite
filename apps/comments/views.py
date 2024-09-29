from apps.comments.forms import CommentForm
from apps.comments.models import Comment, CommentPhotos
from apps.blogs.models import ArticlesModel
from apps.documents.models import DocumentsModel
from apps.photos.views import photos_save
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Likes
from django.db.models import Count


class CommentView():
    model_comments = Comment
    model_photos = CommentPhotos
    form_class = CommentForm

    def comment_get(content_type, object_id):
        comments = CommentView.model_comments.objects.filter(content_type=content_type, object_id=object_id, parent__isnull=True)
        comments = comments.annotate(
            like_count=Count('likes', distinct=True),
        )
        comments = comments.order_by('-likes')
        return comments
    
    def comment_post(request, content_type, object_id, parent_id=None):
        form = CommentView.form_class(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            images = request.FILES.getlist('images')
            for image in images:
                CommentView.model_photos.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(comment),
                    object_id=comment.id,
                    image=image
                )

    def delete_comment(request, comment_id):
        # Yorum nesnesini al
        comment = get_object_or_404(Comment, id=comment_id)

        # Kullanıcının yorum silme yetkisini kontrol et
        if comment.user == request.user or request.user.is_superuser:
            # Yorum sil
            comment.delete()

            content_url = comment.content_object.get_notifications_comment_context()['content_url']
            # content_object üzerinden dinamik olarak yönlendirme yap
            return redirect(content_url)  # Modelde get_absolute_url metodunu kullanarak yönlendiriyoruz

        # Yetki yoksa bir yere yönlendir veya hata fırlat
        return redirect('some_error_page')  # Hata sayfasına yönlendirme (örnek)


class CommentCommentsView(View):
    model_comment = Comment
    model_likes = Likes
    context = {
        'siteTitle': 'Paylaşımlar',
    }
    def get(self, request, comment_id):
        comments = CommentView.model_comments.objects.get(id=comment_id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        content = comments.content_object.get_notifications_comment_context()
        form = CommentView.form_class()
        self.context.update({
            'comments' : comments,
            'liked_comment' : liked_comment,
            'form' : form,
            'content' : content,
            
        })
        return render(request, 'comments/comment-comments.html', self.context)
    
    def post(self, request, comment_id):
        comments = CommentView.model_comments.objects.filter(id=comment_id).first()
        form = CommentView.comment_post(request=request, content_type=comments.content_type, object_id=comments.object_id, parent_id=comments.id)

        self.context.update({
            'comments' : comments,
            'form' : form
        })
        return render(request, 'comments/comment-comments.html', self.context)