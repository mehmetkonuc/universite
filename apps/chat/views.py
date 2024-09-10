from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
# def chat_view(request, chat_id):
#     chat = Chat.objects.get(id=chat_id)
#     # Mesaj gönderme formu
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.chat = chat
#             message.save()
#             return redirect('chat_view', chat_id=chat.id)  # Aynı sohbet sayfasına yeniden yönlendir
#     else:
#         form = MessageForm()

#     messages = chat.messages.order_by('timestamp')
    
#     grouped_messages = []
#     current_user = None
#     current_group = []

#     for message in messages:
#         if message.sender == current_user:
#             current_group.append(message)
#         else:
#             if current_group:
#                 grouped_messages.append((current_user, current_group))
#             current_user = message.sender
#             current_group = [message]
    
#     if current_group:
#         grouped_messages.append((current_user, current_group))

#     context = {
#         'grouped_messages': grouped_messages,
#         'current_user': request.user,
#         'form': form,

#     }
#     return render(request, 'chat/chat_detail.html', context)







def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Eğer kullanıcı bu sohbetin bir parçası değilse, erişim izni verilmesin
    if request.user not in chat.participants.all():
        return redirect('chat_list')  # Kullanıcının sohbet listesine yönlendirebilirsin
    
    other_participant = chat.participants.exclude(id=request.user.id).first()

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

    messages = chat.messages.all().order_by('timestamp')  # Eski mesajları sırala

    return render(request, 'chat/chat_detail.html', {
        'chat': chat,
        'grouped_messages': messages,
        'form': form,
        'other_participant': other_participant,
    })

@login_required
def chat_list(request):
    # Tüm sohbetleri getir
    chats = Chat.objects.filter(participants=request.user)

    # Her sohbet için diğer katılımcıları listele
    chat_data = []
    for chat in chats:
        other_participant = chat.participants.exclude(id=request.user.id).first()  # request.user haricindeki katılımcı
        chat_data.append({
            'chat': chat,
            'other_participant': other_participant
        })

    return render(request, 'chat/chat_list.html', {
        'chat_data': chat_data,
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
