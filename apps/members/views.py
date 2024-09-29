from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .filters import MemberFilter
from django.forms.models import model_to_dict
from .models import MembersFilterModel
from .forms import UserFilterForm

# Create your views here.
class MembersView(View):
    user_filter_model = MembersFilterModel
    user_filter_form = UserFilterForm
    filter_form = MemberFilter
    template = 'members.html'
    context = {
        'siteTitle': 'Üyeler',
    }
    
    def get(self, request):
        user_filter, created = self.user_filter_model.objects.get_or_create(user=request.user)

        members = User.objects.all().exclude(id=request.user.id)  # Varsayılan kullanıcı modelini al

        # Apply filters
        filter = self.filter_form(model_to_dict(user_filter), queryset=members, request=request)
        filtered_data = filter.qs

        # Apply sorting
        sorted_data = filtered_data

        paginator = Paginator(sorted_data, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        self.context.update({
            'members': page_obj,
            'filter': filter,
            'user_filter': user_filter,
            })
        
        return render(request, self.template, self.context)

    def post(self, request):
        user_filter = self.user_filter_model.objects.get(user=request.user)
        if 'reset_filter' in request.POST:
            # Tüm filtre alanlarını temizle
            for field in model_to_dict(user_filter).keys():
                if field not in ['id', 'user']:  # user ve id hariç tüm alanları temizle
                    setattr(user_filter, field, None)
            user_filter.save()
            return self.get(request)
        else:
            form = self.user_filter_form(request.POST, instance = user_filter)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.user=request.user
                form_data.save()

            members = User.objects.all().exclude(id=request.user.id)  # Varsayılan kullanıcı modelini al

            filter = self.filter_form(data=request.POST, queryset=members, request=request)
            filtered_data = filter.qs

            # Apply sorting
            sorted_data = filtered_data
            
            # Pagination
            paginator = Paginator(sorted_data, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            self.context.update({
                'members': page_obj,
                'filter': filter,
                'user_filter': user_filter,
            })
        
        return render(request, self.template, self.context)