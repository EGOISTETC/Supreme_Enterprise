import uuid
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import *


class allviews():
    def redirect_main(request):
        user_id = request.session.get('user_id')
        if user_id:
            user = Client.objects.get(Id=user_id)
            return render(request, "working.html", {'user': user,
                                                    'Login': user.Login
                                                    })
        else:
            return render(request, "working.html", {'user': None})

    def redirect_stat(request):
        user_id = request.session.get('user_id')
        if user_id:
            user = Client.objects.get(Id=user_id)
            return render(request, "stat.html", {'user': user,
                                                 'Login': user.Login
                                                 })
        else:
            return render(request, "stat.html", {'user': None})

    def redirect_registration(request):
        user_id = request.session.get('user_id')
        if user_id:
            user = Client.objects.get(Id=user_id)
            return render(request, "registration.html", {'user': user,
                                                         'Login': user.Login
                                                         })
        else:
            return render(request, "registration.html", {'user': None})

    def redirect_authorization(request):
        user_id = request.session.get('user_id')
        if user_id:
            user = Client.objects.get(Id=user_id)
            return render(request, "login.html", {'user': user,
                                                  'Login': user.Login
                                                  })
        else:
            return render(request, "login.html", {'user': None})

    def redirect_services(request):
        user_id = request.session.get('user_id')
        if user_id:
            user = Client.objects.get(Id=user_id)

            return render(request, "service.html", {'user': user,
                                                    'Login': user.Login
                                                    })
        else:
            return render(request, "main.html", {'user': None})

    def redirect_pay(request):
        user_id = request.session.get('user_id')
        if user_id:
            user = Client.objects.get(Id=user_id)
            return render(request, "oplata.html", {'user': user,
                                                   'Login': user.Login
                                                   })
        else:
            return render(request, "oplata.html", {'user': None})

    def redirect_cabinet(request):
        user_id = request.session.get('user_id')
        if user_id:
            user = Client.objects.get(Id=user_id)
            return render(request, "main.html", {'user': user,
                                                 'Login': user.Login
                                                 })
        else:
            return render(request, "main.html", {'user': None})

    def logout(request):
        request.session.clear()
        return redirect('go_to_auth')

    @csrf_exempt
    def update_analytics(request):
        if request.method == 'POST':
            data = request.POST
            channel = data.get('channel')
            messages_count = data.get('messages_count')
            keyword_matches = data.get('keyword_matches')
            members_count = data.get('members_count')
            relevance = data.get('relevance')

            Analytics.objects.filter(channel=channel).delete()

            analytics_obj = Analytics.objects.create(
                channel=channel,
                messages_count=messages_count,
                members_count=members_count,
                keyword_matches=keyword_matches,
                relevance=relevance
            )
            analytics_obj.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(status=400)


class register():
    def reg(request):
        if request.method == 'POST':
            first_name = request.POST.get("first_name")
            phone = request.POST.get("phone")
            login = request.POST.get("login")
            password = request.POST.get("password")
            user_exists = Client.objects.filter(Phone_Numder=phone).exists()
            if not user_exists:
                user = Client.objects.create(
                    First_Name=first_name,
                    Last_Name='',
                    Phone_Numder=phone,
                    Login=login,
                    Password=password,
                    Massanger="None",
                    Jwt_Token=uuid.uuid4(),
                    Referal_Url_id=3,
                    Tarif_Active=True
                )
                request.session['user_id'] = user.Id
                return redirect('cabinet')
            else:
                return JsonResponse({'status': 'error', 'message': 'Номер занят'}, status=400)


class LoginView():
    def auth(request):
        if request.method == 'POST':
            login = request.POST.get('login')
            password = request.POST.get('password')
            user = Client.objects.filter(Login=login, Password=password).first()
            if user:
                request.session['user_id'] = user.Id
                return redirect('cabinet')
            else:
                return redirect('go_to_auth', {'message': 'Пользователя с такими данными не существует'})


class AnalyticsView():
    def get_analytics(request):
        analytics_data = []
        analytics_objects = Analytics.objects.all()
        for obj in analytics_objects:
            analytics_data.append({
                'channel': obj.channel,
                'messages_count': obj.messages_count,
                'members_count': obj.members_count,
                'keyword_matches': obj.keyword_matches,
                'relevance': obj.relevance
            })
        print(analytics_data)
        return JsonResponse(analytics_data, safe=False)
