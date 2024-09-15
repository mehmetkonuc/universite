from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q, Max
from .models import Message, Chat
from django.template.loader import render_to_string
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    chats = Chat.objects.filter(
        Q(first_user=request.user) | Q(second_user=request.user)
    ).annotate(
        last_message_time=Max('message__timestamp')
    ).order_by('-last_message_time')
    chat_list = []
    for chat in chats:
        messages = Message.objects.filter(chat=chat, receiver=request.user, is_read=False)
        if messages:
            is_read = False
        else:
            is_read = True
        chat_list.append({'chat':chat, 'is_read': is_read})
    return render(request, 'chat/index.html', {'chats':chat_list})

def start_chat(request, second_user_id=None):
    first_user = request.user
    second_user = get_object_or_404(User, pk=second_user_id)
        
    # Check if a chat already exists between these two users (regardless of who initiated it)
    chat = Chat.objects.filter(
        (Q(first_user=first_user, second_user=second_user) | Q(first_user=second_user, second_user=first_user))
    ).first()
    if chat:
        return redirect('chat', chat.id)
    else:
        chat = Chat.objects.create(first_user=first_user, second_user=second_user)
        return redirect('chat', chat.id)

def chat(request, chat_id):
    chats = Chat.objects.filter(
        Q(first_user=request.user) | Q(second_user=request.user)
    ).distinct()
    chat_user = chats.get(id=chat_id)
    chats = chats.annotate(
        last_message_time=Max('message__timestamp')
    ).order_by('-last_message_time')
    chat_list = []
    for chat in chats:
        messages = Message.objects.filter(chat=chat)
        if messages.exists():
            message = messages.filter(chat=chat, receiver=request.user, is_read=False)
            if message:
                is_read = False
            else:
                is_read = True
            chat_list.append({'chat':chat, 'is_read': is_read})



    # chats = [chat for chat in chats if Message.objects.filter(chat=chat).exists()]
    messages = Message.objects.filter(chat=chat_user)

    return render(request, 'chat/index.html', {'chats' : chat_list, 'chat':chat_user, 'messages':messages})

def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        chat_id = request.POST.get('chat_id')

        if message_text and chat_id:
            receiver = Chat.objects.get(id=chat_id)
            if receiver.first_user == request.user:
                Message.objects.create(content=message_text, sender=request.user, receiver=receiver.second_user, chat=receiver)
            else:
                Message.objects.create(content=message_text, sender=request.user, receiver=receiver.first_user, chat=receiver)

            return JsonResponse({'status': 'Message sent successfully'})
        else:
            return JsonResponse({'error': 'Message or second user ID missing'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    


@csrf_exempt
def get_messages(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chat_id = data.get('chat_id')
            chat = Chat.objects.get(id=chat_id)
            messages = Message.objects.filter(chat=chat).order_by('timestamp')
            read = messages.filter(receiver=request.user, is_read=False).update(is_read=True)
            
            context={
                'chat':chat,
                'messages': messages,
                'user': request.user,
            }
            # Render the messages to the template
            html = render_to_string('chat/messages.html', context)
            
            return JsonResponse({'html': html})
        except (Chat.DoesNotExist, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)