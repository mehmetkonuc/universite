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

        self.context.update(
            {'members': members,
                }
        )
        
        return render(request, self.template, self.context)