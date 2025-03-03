from django.shortcuts import render, redirect
from django.views import View
from .forms import PostsForm, FilterForm
from .models import PostsModel, PostsFilterModel, PostsPhotos
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Likes
from apps.comments.views import CommentView
from .filters import Filter
from django.db.models import Count
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.contrib import messages


class PostView(View):
    model_post = PostsModel
    model_like = Likes
    form_post = PostsForm
    model_filter = PostsFilterModel
    filter_form = FilterForm
    filter = Filter
    model_photos = PostsPhotos
    template_name = 'post.html'
    context = {
        'siteTitle': 'Paylaşımlar',
    }
    paginate_by = 2
    
    def get(self, request):
        if request.user.is_authenticated:
            user_filter, created = self.model_filter.objects.get_or_create(user=request.user)
            data = self.model_post.objects.filter().order_by('-create_at')
            
            data = data.annotate(
                like_count=Count('likes', distinct=True),
                comment_count=Count('comments', distinct=True)
            )

            # Apply filters
            filter = self.filter(model_to_dict(user_filter), queryset=data, request=request)
            filtered_data = filter.qs

            # Apply sorting
            sorted_data = filtered_data

            # Pagination
            paginator = Paginator(sorted_data, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            post_ids = page_obj.object_list.values_list('id', flat=True)

            content_type = ContentType.objects.get_for_model(self.model_post)
            liked = self.model_like.objects.filter(
                content_type=content_type, user = request.user, object_id__in=post_ids
            ).values_list('object_id', flat=True)

            form = self.form_post()

            self.context.update({
                'forms': form,
                'data': page_obj,
                'filter': filter,
                'user_filter': user_filter,
                'liked': liked,
            })
            
            return render(request, self.template_name, self.context)
        else:
            return render(request, 'visitor/home/guest.html')
        
    def post(self, request):
        if request.user.is_authenticated:
            user_filter = self.model_filter.objects.get(user=request.user)
            if 'reset_filter' in request.POST:
                # Tüm filtre alanlarını temizle
                for field in model_to_dict(user_filter).keys():
                    if field not in ['id', 'user']:  # user ve id hariç tüm alanları temizle
                        setattr(user_filter, field, None)
                user_filter.save()
                messages.success(request, 'Filtre sıfırlandı.')

                return self.get(request) 
            else:
                form = self.form_post(request.POST)
                if form.is_valid():
                    images = request.FILES.getlist('images')
                    if form.cleaned_data['content'] or images:
                        form_save = form.save(commit=False)
                        form_save.user = request.user
                        form_save.save()
                        for image in images:
                            self.model_photos.objects.create(
                                user=request.user,
                                content_type=ContentType.objects.get_for_model(form_save),
                                object_id=form_save.pk,
                                image=image
                                )
                        return redirect('home')
                    else:
                        form_filter = self.filter_form(request.POST, instance = user_filter)
                        if form_filter.is_valid():
                            form_data = form_filter.save(commit=False)
                            form_data.user=request.user
                            form_data.save()
                            messages.success(request, 'Filtre uygulandı ve kaydedildi.')


                data = self.model_post.objects.filter().order_by('-create_at')
                data = data.annotate(
                    like_count=Count('likes', distinct=True),
                    comment_count=Count('comments', distinct=True)
                    )  
                
                filter = self.filter(model_to_dict(user_filter), queryset=data, request=request)
                filtered_data = filter.qs

                # Apply sorting
                sorted_data = filtered_data

                # Pagination
                paginator = Paginator(sorted_data, self.paginate_by)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                post_ids = page_obj.object_list.values_list('id', flat=True)

                content_type = ContentType.objects.get_for_model(self.model_post)
                liked = self.model_like.objects.filter(
                    content_type=content_type, user = request.user, object_id__in=post_ids
                ).values_list('object_id', flat=True)

                self.context.update({
                    'data': page_obj,
                    'form': form,
                    'filter': filter,
                    'user_filter': user_filter,
                    'liked': liked,
                })

            return render(request, self.template_name, self.context)


def delete_post(request, PostID):
    delete_post = PostsModel.objects.get(id=PostID)
    
    if delete_post.user == request.user or request.user.is_superuser:
        delete_post.delete()
        
    return redirect('post')

class PostDetails(View):
    model_posts = PostsModel
    model_likes = Likes
    paginate_by = 2
    template = 'post-detail.html'
    context = {
        'siteTitle': 'Yorumlar',
    }
    def get(self, request, post_id):
        post = self.model_posts.objects.filter(id=post_id).prefetch_related('likes', 'comments').first()
        liked = post.likes.filter(user=request.user)
        comments = post.comments.filter(parent__isnull=True)

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        post_ids = page_obj.object_list.values_list('id', flat=True)

        liked_comment = self.model_likes.objects.filter(
            content_type=ContentType.objects.get_for_model(CommentView.model_comments),
            user=request.user,
            object_id__in=post_ids,
            ).values_list('object_id', flat=True)
        
        form = CommentView.form_class()


        self.context.update({
            'form': form,
            'post' : post,
            'comments' : page_obj,
            'liked':liked,
            'liked_comment': liked_comment,
        })
        return render(request, self.template, self.context)
    
    def post(self, request, post_id):
        post = self.model_posts.objects.filter(id=post_id).first()
        liked = post.likes.filter(user=request.user)

        content_type = ContentType.objects.get_for_model(post)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=post_id)

        comments = post.comments.filter(parent__isnull=True)

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        post_ids = page_obj.object_list.values_list('id', flat=True)

        liked_comment = self.model_likes.objects.filter(
            content_type=ContentType.objects.get_for_model(CommentView.model_comments),
            user=request.user,
            object_id__in=post_ids,
            ).values_list('object_id', flat=True)


        self.context.update({
            'form': form,
            'post' : post,
            'comments' : page_obj,
            'liked':liked,
            'liked_comment': liked_comment,
            })
        return render(request, self.template, self.context)