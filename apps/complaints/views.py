from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComplaintForm
from .models import Complaint
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test

def file_complaint(request, app_label, model, object_id):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            # ContentType ve object_id ile şikayet edilen içeriği belirle
            content_type = ContentType.objects.get(app_label=app_label, model=model.lower())
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.content_type = content_type
            complaint.object_id = object_id
            complaint.save()
            return redirect('success_page')  # Şikayet başarılı sayfasına yönlendirme
    else:
        form = ComplaintForm()

    return render(request, 'complaints/file_complaint.html', {'form': form})




@user_passes_test(lambda u: u.is_superuser)
def view_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, 'complaints/view_complaints.html', {'complaints': complaints})
