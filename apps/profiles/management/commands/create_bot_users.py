
# management/commands/create_bot_users.py
import random
import requests
from io import BytesIO
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker
from apps.profiles.models import (
    EducationalInformationModel, 
    ProfilePictureModel, 
    PrivacyModel
)
from apps.inputs.models import CountriesModel, UniversitiesModel, DepartmentsModel, StatusModel

class Command(BaseCommand):
    help = 'Cinsiyet-uyumlu yüksek çözünürlüklü bot kullanıcılar oluşturur'

    def get_gender_specific_name(self, fake):
        """Cinsiyete göre isim üretir ve cinsiyeti döndürür"""
        gender = random.choice(['male', 'female'])
        first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
        last_name = fake.last_name()
        return first_name, last_name, gender

    def download_highres_image(self, gender, retry=3):
        """Yüksek çözünürlüklü ve cinsiyet-uyumlu resim indir"""
        base_url = "https://randomuser.me/api/portraits/"
        size_options = ['med', 'large']  # Öncelik sırası
        
        for size in size_options:
            try:
                img_num = random.randint(0, 99)
                url = f"{base_url}{size}/{'men' if gender == 'male' else 'women'}/{img_num}.jpg"
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                return response.content
            except:
                if retry > 0:
                    return self.download_highres_image(gender, retry-1)
        return None

    def handle(self, *args, **kwargs):
        fake = Faker('tr_TR')
        
        # Veritabanı ilişkileri
        COUNTRIES = list(CountriesModel.objects.all())
        UNIVERSITIES = list(UniversitiesModel.objects.all())
        DEPARTMENTS = list(DepartmentsModel.objects.all())
        STATUSES = list(StatusModel.objects.all())

        with transaction.atomic():
            for i in range(3):
                # Cinsiyet-uyumlu isim üret
                first_name, last_name, gender = self.get_gender_specific_name(fake)
                
                # Kullanıcı oluştur
                user = User.objects.create_user(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    first_name=first_name,
                    last_name=last_name,
                    password='botpassword123'
                )

                # Yüksek çözünürlüklü resim indir
                try:
                    image_content = self.download_highres_image(gender)
                    if image_content:
                        img_io = BytesIO(image_content)
                        profile = ProfilePictureModel(user=user)
                        profile.profile_photo.save(
                            f"profile_{user.id}_hr.jpg",
                            File(img_io)
                        )
                    else:
                        raise Exception("Resim indirilemedi")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Fallback: {e}"))
                    # Fallback 1: Cinsiyet-uyumlu küçük resim
                    img_num = random.randint(0, 99)
                    fallback_url = f"https://randomuser.me/api/portraits/med/{'men' if gender == 'male' else 'women'}/{img_num}.jpg"
                    ProfilePictureModel.objects.create(
                        user=user,
                        profile_photo=fallback_url
                    )

                # İlişkisel veri seçimi
                country = random.choice(COUNTRIES)
                
                # Seçilen ülkeye ait üniversiteler
                country_universities = UniversitiesModel.objects.filter(countries=country)
                university = random.choice(country_universities) if country_universities else random.choice(UNIVERSITIES)
                
                # Seçilen üniversiteye ait bölümler
                university_departments = DepartmentsModel.objects.filter(universities=university)
                department = random.choice(university_departments) if university_departments else random.choice(DEPARTMENTS)


                # Eğitim bilgileri
                EducationalInformationModel.objects.create(
                    user=user,
                    country=country,
                    university=university,
                    department=department,
                    status=random.choice(STATUSES)
                )

                # Gizlilik ayarı
                PrivacyModel.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS('2000 uyumlu kullanıcı oluşturuldu!'))