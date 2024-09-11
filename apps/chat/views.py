from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def chat_view(request, chat_id):
    chats = Chat.objects.filter(participants=request.user)
    chat = get_object_or_404(chats, id=chat_id)

    # Eğer kullanıcı bu sohbetin bir parçası değilse, erişim izni verilmesin
    if request.user not in chat.participants.all():
        return redirect('chat_list')  # Kullanıcının sohbet listesine yönlendirebilirsin

    # Mesaj gönderme formu
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = chat
            message.save()
            return redirect('chat_view', chat_id=chat.id)  # Aynı sohbet sayfasına yeniden yönlendir
    else:
        form = MessageForm()

    chat_data = []
    for data in chats:
        if data.messages.count() > 0:
            other_participant = data.participants.exclude(id=request.user.id).first()  # request.user haricindeki katılımcı
            chat_data.append({
                'chat': chat,
                'other_participant': other_participant
            })

    messages = chat.messages.all().order_by('timestamp')  # Eski mesajları sırala

    return render(request, 'chat/chat_detail.html', {
        'chat': chat,
        'chats': chat_data,
        'messages': messages,
        'form': form,
    })

@login_required
def chat_list(request):
    # Tüm sohbetleri getir
    chats = Chat.objects.filter(participants=request.user)

    # Her sohbet için diğer katılımcıları listele
    chat_data = []
    for chat in chats:
        if chat.messages.count() > 0:
            other_participant = chat.participants.exclude(id=request.user.id).first()  # request.user haricindeki katılımcı
            chat_data.append({
                'chat': chat,
                'other_participant': other_participant
            })

    return render(request, 'chat/chat_list.html', {
        'chats': chat_data,
    })



@login_required
def start_chat(request, user_id):
    user_to_chat = get_object_or_404(User, id=user_id)

    # Zaten bir sohbet var mı kontrol et
    existing_chat = Chat.objects.filter(participants=request.user).filter(participants=user_to_chat).first()

    if existing_chat:
        return redirect('chat_view', chat_id=existing_chat.id)

    # Yeni sohbet oluştur
    new_chat = Chat.objects.create()
    new_chat.participants.add(request.user, user_to_chat)
    new_chat.save()

    return redirect('chat_view', chat_id=new_chat.id)


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)

    return render(request, 'chat/user_list.html', {
        'users': users,
    })
