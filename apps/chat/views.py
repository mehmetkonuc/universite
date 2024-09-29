from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.db.models import Q, Max
from .models import Message, Chat
from django.template.loader import render_to_string
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from apps.follow.models import Follow
from django.utils.html import escape

def index(request):
    chats = Chat.objects.filter(
        Q(first_user=request.user) | Q(second_user=request.user)
    ).annotate(
        last_message_time=Max('message__timestamp')
    ).order_by('-last_message_time')
    
    chat_list = []
    for chat in chats:
        # Mesaj var mı kontrol et, yoksa chat'i atla
        if Message.objects.filter(chat=chat).exists():
            # Okunmamış mesaj var mı kontrol et
            is_read = not Message.objects.filter(chat=chat, receiver=request.user, is_read=False).exists()
            chat_list.append({'chat': chat, 'is_read': is_read})

    return render(request, 'chat/index.html', {'chats': chat_list})



def start_chat(request, username=None):
    first_user = request.user
    second_user = get_object_or_404(User, username=username)
    
    # Kullanıcının mesaj gizlilik ayarını al
    message_privacy = second_user.privacy.message_privacy

    # Eğer kullanıcı "nobody" seçeneğini seçtiyse 404 hatası döndür
    if message_privacy == 'nobody':
        raise Http404("Bu kullanıcıya mesaj gönderemezsiniz.")
    
    # Eğer gizlilik ayarı "everyone" ise sohbeti başlat
    if message_privacy == 'everyone':
        # Mevcut bir sohbet olup olmadığını kontrol et
        chat = Chat.objects.filter(
            Q(first_user=first_user, second_user=second_user) | Q(first_user=second_user, second_user=first_user)
        ).first()
        if chat:
            return redirect('chat', chat.id)
        else:
            chat = Chat.objects.create(first_user=first_user, second_user=second_user)
            return redirect('chat', chat.id)
        
    # Eğer gizlilik ayarı "followers" ise takip ilişkisini kontrol et
    elif message_privacy == 'followers':
        is_following = second_user.followers.filter(follower=first_user).exists()  # İkinci kullanıcının takipçileri arasında birinci kullanıcı var mı kontrol et
        if is_following:
            # Mevcut bir sohbet olup olmadığını kontrol et
            chat = Chat.objects.filter(
                Q(first_user=first_user, second_user=second_user) | Q(first_user=second_user, second_user=first_user)
            ).first()
            if chat:
                return redirect('chat', chat.id)
            else:
                chat = Chat.objects.create(first_user=first_user, second_user=second_user)
                return redirect('chat', chat.id)
        else:
            raise Http404("Bu kullanıcıya sadece takipçileri mesaj gönderebilir.")
        

def chat(request, chat_id):
    # Kullanıcıya ait tüm chatleri al
    chats = Chat.objects.filter(
        Q(first_user=request.user) | Q(second_user=request.user)
    ).distinct()

    # Chat'i ID'ye göre al, eğer yoksa 404 döndür
    chat_user = get_object_or_404(chats, id=chat_id)


    # Okunmamış mesajları güncelle
    Message.objects.filter(chat=chat_user, receiver=request.user, is_read=False).select_related('receiver').update(is_read=True)

    # En son 10 mesajı çek
    messages = Message.objects.filter(chat=chat_user).order_by('-timestamp')[:20].select_related('receiver')
    messages = messages[::-1]


    # Son mesaj zamanına göre sıralı chat listesini hazırla
    chats = chats.annotate(
        last_message_time=Max('message__timestamp')
    ).order_by('-last_message_time')

    # Chat listesi oluştur, is_read durumunu tek bir sorguyla al
    chat_list = []
    for chat in chats:
        # Mesaj var mı kontrol et, yoksa chat'i atla
        if Message.objects.filter(chat=chat).exists():
            # Okunmamış mesaj var mı kontrol et
            is_read = not Message.objects.filter(chat=chat, receiver=request.user, is_read=False).exists()
            chat_list.append({'chat': chat, 'is_read': is_read})

    # Şablona gönderilecek context
    context = {
        'chats': chat_list,
        'chat': chat_user,
        'data': messages
    }

    return render(request, 'chat/index.html', context)


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
            # messages = Message.objects.filter(chat=chat).order_by('timestamp')
            # En yeni 20 mesajı çek (örneğin)
            # messages = Message.objects.filter(chat=chat).order_by('-timestamp')[:20]
            # messages = messages[::-1]  # En son mesajı aşağıda göstermek için ters çeviriyoruz
            # read = messages.filter(receiver=request.user, is_read=False).update(is_read=True)

            # Okunmamış mesajları güncelle
            Message.objects.filter(chat=chat, receiver=request.user, is_read=False).select_related('receiver').update(is_read=True)

            # En son 10 mesajı çek
            messages = Message.objects.filter(chat=chat).order_by('-timestamp')[:20].select_related('receiver')
            messages = messages[::-1]



            context={
                'chat':chat,
                'data': messages,
                'user': request.user,
            }
            # Render the messages to the template
            html = render_to_string('chat/messages.html', context)
            
            return JsonResponse({'html': html})
        except (Chat.DoesNotExist, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)



# @login_required
def messages_mark_all_as_read(request):
    if request.method == 'POST':
        Message.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def delete_chat(request, chat_id):
    Message.objects.filter(chat_id=chat_id).delete()
    # Chat.objects.get(id=chat_id).delete()
    messages.success(request, 'Sohbet Başarıyla silindi.')

    return redirect('chat_index')




def get_older_messages(request):
    chat_id = request.GET.get('chat_id')
    last_message_id = request.GET.get('last_message_id')
    chat = get_object_or_404(Chat, id=chat_id)
    user = request.user

    # last_message_id'den daha eski 20 mesajı çek
    messages = Message.objects.filter(chat=chat, id__lt=last_message_id).order_by('-timestamp')[:20].select_related('receiver')
    messages = messages[::-1]  # En eski mesajı yukarıda göstermek için ters çeviriyoruz
    
    # Eski mesajları HTML olarak render et
    rendered_messages = render_to_string('chat/partial.html', {'data': messages, 'user':user})


    return JsonResponse({'html': rendered_messages})