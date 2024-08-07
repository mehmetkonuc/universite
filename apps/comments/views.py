from apps.comments.forms import CommentForm
from apps.comments.models import Comment
from django.shortcuts import redirect
from apps.blogs.models import ArticlesModel
from apps.photos.views import photos_save
# Create your views here.

class CommentView():
    model_comments = Comment
    form_class = CommentForm

    def comment_get(content_type, object_id):
        comments = CommentView.model_comments.objects.filter(content_type=content_type, object_id=object_id).order_by('-created_at')
        return comments
    
    def comment_post(request, content_type, object_id):
        form = CommentView.form_class(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            comment.save()
            photos_save(request=request, model=comment)

    def delete_comment(request, comment_id):
        delete_comment = Comment.objects.get(id=comment_id)
        if delete_comment.user == request.user or request.user.is_superuser:
            delete_comment.delete()
            
        if 'Post' in str(delete_comment.content_type):
            return redirect('post_detail', post_id=delete_comment.object_id)
        
        elif 'Blogs' in str(delete_comment.content_type):
            article = ArticlesModel.objects.get(id=delete_comment.object_id)
            return redirect('article_details', slug=article.slug)
