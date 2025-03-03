# complaints/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComplaintForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Complaint
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

@login_required
def create_complaint(request, app_name, model_name, object_id):
    content_type = get_object_or_404(ContentType, app_label=app_name, model=model_name.lower())
    content_object = content_type.get_object_for_this_type(pk=object_id)
    
    if request.method == "POST":
        form = ComplaintForm(request.POST, user=request.user, content_object=content_object)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.content_object = content_object
            complaint.save()
            messages.success(request, 'Şikayet Başarıyla Gönderildi')
            return redirect('home')
    else:
        form = ComplaintForm(user=request.user, content_object=content_object)
    
    return render(request, 'complaints/create_complaint.html', {
        'form': form,
        'content_object': content_object
    })


@staff_member_required
def complaint_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Filtreleme
    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if category_filter:
        complaints = complaints.filter(category=category_filter)
    
    # Sayfalama
    paginator = Paginator(complaints, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Complaint.STATUS_CHOICES,
        'category_choices': Complaint.COMPLAINT_CATEGORIES,
        'current_status': status_filter,
        'current_category': category_filter
    }
    return render(request, 'complaints/admin_dashboard.html', context)

@staff_member_required
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes')
        
        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            complaint.admin_notes = admin_notes
            complaint.save()
            messages.success(request, 'Durum başarıyla güncellendi')
        else:
            messages.error(request, 'Geçersiz durum seçimi')
        
    return redirect('complaint_dashboard')


@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    # Filtreleme ve sayfalama
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    paginator = Paginator(complaints, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'complaints/my_complaints.html', {
        'page_obj': page_obj,
        'status_choices': Complaint.STATUS_CHOICES,
        'current_status': status_filter
    })


@login_required
@require_POST
def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, user=request.user)
    complaint.delete()
    messages.success(request, "Şikayetiniz başarıyla silindi")
    return redirect('my_complaints')