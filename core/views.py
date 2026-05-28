import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TelegramForm
from .models import SiteConfig
from decouple import config  # .env dan olish uchun

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_to_telegram(request):
    # 1. Avval Admin paneldan olishga harakat qilamiz
    site_config = SiteConfig.objects.first()
    
    # Agar admin panelda ma'lumot bo'lmasa, .env dan olamiz
    if not site_config or not site_config.bot_token or not site_config.chat_id:
        bot_token = config('BOT_TOKEN', default=None)
        chat_id = config('CHAT_ID', default=None)
        use_env = True
    else:
        bot_token = site_config.bot_token
        chat_id = site_config.chat_id
        use_env = False

    if not bot_token or not chat_id:
        messages.error(request, "⚠️ Bot token yoki Chat ID sozlanmagan!")
        return render(request, 'core/index.html', {'form': TelegramForm()})

    if request.method == 'POST':
        form = TelegramForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'] or 'Anonim'
            message_text = form.cleaned_data['message']
            file = request.FILES.get('file')
            ip = get_client_ip(request)

            text = f"""
🆕 Yangi xabar!

👤 Ism: {name}
🌐 IP: {ip}
📝 Xabar: 
{message_text}
            """.strip()

            try:
                # Matn yuborish
                response1 = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                    timeout=10
                )

                # Fayl yuborish
                if file:
                    dangerous_ext = ['.exe', '.bat', '.cmd', '.scr', '.js', '.vbs', '.ps1', '.pif']
                    if any(file.name.lower().endswith(ext) for ext in dangerous_ext):
                        messages.error(request, "❌ Bu turdagi fayl yuborish taqiqlangan!")
                        return render(request, 'core/index.html', {'form': form})

                    if file.size > 50 * 1024 * 1024:
                        messages.error(request, "❌ Fayl hajmi 50MB dan oshmasligi kerak!")
                        return render(request, 'core/index.html', {'form': form})

                    files = {'document': (file.name, file, file.content_type)}
                    response2 = requests.post(
                        f"https://api.telegram.org/bot{bot_token}/sendDocument",
                        data={'chat_id': chat_id, 'caption': f"📎 {name} dan | IP: {ip}"},
                        files=files,
                        timeout=30
                    )

                messages.success(request, "✅ Xabaringiz muvaffaqiyatli yuborildi!")
                return redirect('home')

            except Exception as e:
                messages.error(request, f"❌ Xatolik yuz berdi: {str(e)}")
                print("Telegram Error:", e)  # Konsolda ko'rish uchun

    else:
        form = TelegramForm()

    return render(request, 'core/index.html', {'form': form})