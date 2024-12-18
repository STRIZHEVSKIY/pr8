from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST

from .decorators import custom_login_required, custom_admin_required
from .forms import UserRegisterForm, UserLoginForm, SettingsForm
from .models import User, City, PDFFile
from django.http import HttpResponse
import base64
from faker import Faker

from rest_framework import viewsets
from .serializers import UserSerializer, CitySerializer, PDFFileSerializer


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Используйте set_password для хеширования пароля
            user.save()
            login(request, user)
            return redirect('index')
        else:
            print("Registration form is not valid:", form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Неправильное имя пользователя или пароль.")
        else:
            print("Login form is not valid:", form.errors)
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')



@custom_login_required
def city_list(request):
    books = City.objects.all()
    return render(request, 'city_list.html', {'books': books})


@custom_login_required
def city_details(request, id):
    book = get_object_or_404(City, id=id)
    return render(request, 'city_details.html', {'book': book})


@custom_admin_required
def upload_pdf(request):
    if request.method == 'POST':
        file = request.FILES['pdf_file']
        if file.content_type == 'application/pdf':
            PDFFile.objects.create(
                name=file.name,
                mime_type=file.content_type,
                file_data=file.read()
            )
            return redirect('index')
        else:
            return redirect('index')
    return render(request, 'upload_pdf.html')


@custom_login_required
def download_list(request):
    files = PDFFile.objects.all()
    return render(request, 'download_pdf_list.html', {'files': files})


@custom_login_required
def download_pdf(request, id):
    file = get_object_or_404(PDFFile, id=id)
    response = HttpResponse(file.file_data, content_type=file.mime_type)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response


@require_POST
def save_image(request):
    data = request.body.decode('utf-8')
    image_data = data.replace('data:image/png;base64,', '')
    image_data = base64.b64decode(image_data)

    response = HttpResponse(content_type="image/png")
    response.write(image_data)
    return response

@custom_login_required
def statistics(request):
    # Получаем все данные о городах
    cities = City.objects.all()

    # Для графика "Средняя температура"
    average_temperatures = [int(city.Temperature) if city.Temperature.isdigit() else 0 for city in cities]

    # Для графика "Длина описаний погоды"
    weather_lens = [len(city.Weather) for city in cities]

    # Для графика "Количество символов в названии города"
    city_name_lens = [len(city.City) for city in cities]

    # Разделение по диапазонам для средней температуры
    temperature_ranges = [
        len([t for t in average_temperatures if t < 0]),  # Температуры ниже 0
        len([t for t in average_temperatures if 0 <= t < 10]),  # От 0 до 9
        len([t for t in average_temperatures if 10 <= t < 20]),  # От 10 до 19
        len([t for t in average_temperatures if t >= 20]),  # Температуры 20 и выше
    ]

    context = {
        'average_temperatures': average_temperatures,
        'weather_lens': weather_lens,
        'city_name_lens': city_name_lens,
        'temperature_ranges': temperature_ranges,
        'city_names': [city.City for city in cities],
    }
    return render(request, 'statistics.html', context)




@custom_login_required
def generate_fixtures(request):
    fake = Faker()

    # Генерация фиктивных данных
    for _ in range(10):
        # Создаем фиктивные данные для города
        City.objects.create(
            City=fake.city(),
            Temperature=fake.random_int(min=-30, max=40),  # Температура в градусах
            Weather=fake.word()  # Описание погоды (например, "солнечно", "дождливо")
        )

    return redirect('index')


def error_view(request):
    return render(request, 'error.html', status=403)

@custom_login_required
def settings_view(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SettingsForm(instance=request.user)

    context = {
        'form': form,
        'username': request.user.username,
        'user_theme': request.user.theme,
        'user_lang': request.user.lang,
    }
    return render(request, 'settings.html', context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class PDFFileViewSet(viewsets.ModelViewSet):
    queryset = PDFFile.objects.all()
    serializer_class = PDFFileSerializer




