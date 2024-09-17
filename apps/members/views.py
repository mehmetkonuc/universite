from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Create your views here.
class MembersView(View):
    template = 'members.html'
    context = {
        'siteTitle': 'Üyeler',
    }
    
    def get(self, request):
        members = User.objects.all()  # Varsayılan kullanıcı modelini al
        user = request.user
        
        # Kullanıcının takip ettiği kullanıcıları al
        following_users = user.followers.all()
        
        # Takip durumu sözlüğünü oluştur
        member_following_status = {
            member.id: member in following_users
            for member in members
        }
        
        self.context.update(
            {
                'members': members,
                'member_following_status': member_following_status
            }
        )
        
        return render(request, self.template, self.context)