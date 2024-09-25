from django.contrib.auth.models import User
from django.db import models


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_read = models.BooleanField(default=False)  # Bildirim okundu mu?

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'


class FollowRequest(models.Model):
    follower = models.ForeignKey(User, related_name='follow_requests_sent', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follow_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)  # Bildirim okundu mu?

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} requested to follow {self.following}'
