
# Anchora Mall

One-stop solution for your needs!

# Steps of Work - Tugas Individu I
1. Persiapan environment dan inisialisasi project
```bash
vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall$ python3 -m venv .venv
vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall$ source .venv/bin/activate
(.venv) vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall$ nano requirements.txt
(.venv) vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall$ pip install -r requirements.txt
```
Virtual environment dibuat agar dependency proyek isolated sistem global. Aktivasi environment memastikan semua package (seperti Django) terinstall di .venv/. Selain itu, dilakukan instalasi deps yang digunakan melalui file requirements.txt dan pip.

2. Membuat project dan django app
```bash
(.venv) vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall$ django-admin startproject anchora
(.venv) vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall$ cd anchora
(.venv) vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall/anchora$ python3 manage.py startapp main
```
Kemudian lakukan routing pada anchora/urls.py:
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
]
```
Lalu buat routing di main/urls.py:
```python
urlpatterns = [
    path('', show_main, name='show_main'),
]
```
Buat fungsi views pada main/views.py:
```python
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest as Request

# Create your views here.
def show_main(request: Request) -> HttpResponse:
    return render(request, 'main.html')
```

3. Membuat model Product
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    is_official_store = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # for foreign keys preparation
    brand_id = models.UUIDField()
    category_id = models.UUIDField()
    shop_id = models.UUIDField()
    seo_keywords_ids = models.JSONField(default=list)

    def __str__(self):
        return self.name
```

4. Migrasi database
```bash
(.venv) vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall/anchora$ python manage.py makemigrations main
Migrations for 'main':
  main/migrations/0001_initial.py
    + Create model Product
```
Lalu jalankan migrasi:
```bash
(.venv) vincent@DESKTOP-JN0AUB6:~/pbp/individual-assignment/anchora-mall/anchora$ python manage.py migratete
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, main, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying main.0001_initial... OK
  Applying sessions.0001_initial... OK
```

5. Membuat template HTML
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anchora Mall</title>
</head>
<body>
    <h1>Welcome to Anchora Mall</h1>
    <p>Your one-stop shop for everything!</p>
    <p>Vincentius Filbert Amadeo</p>
    <p>2406351711 - PBP E</p>
</body>
</html>
```

6. Tangkapan layar hasil proses
![Screenshot](https://lh3.googleusercontent.com/rd-d/ALs6j_Fo9IBNKGSYGRkLEa6ooPoXho9JlplI6EwS1xM0qnTvv4nhPYkchU9X0xgRVmAsZluUAjyOE8EWXqe3cSP9myYvGbJnAs7tmVO8Lq7C_h-q5tZWCx-YZpTchny5y_SBtIzSIgtie-cLeRjK-WqOmYJE0Opk23EPE92yQmV2sl66gAFSArp2DoDQalRgCZ-7fDxMOvk6FOuAmLOVHM2R8Fe2zQ1EFGF9BUJi7tyDKS7HvxvZT38XyN9emRVAm_qmAZmIaIVSxndPAOqXyw8JluJVR54oGNZsRGv9JlhL6sfo50gB_3CpZI-wjaxgBuqlPrLX37DKSJkZGdTdb4IlKWG7dO0vZITItuwVO6V44KRislxvbAoQS7SCQ5ShLLtriyJVPgQKVEJlUfRd1AojgZIlqk1_YB3E4uv-XzA9Z_zZ0r8GKAqtSTq5rMQ8Bb3krZ-GbbiU5RjgtRj2Zs15VDwrQbZuRXSJS89X1w1PuMwrI59avrA15rGVFlL9N3s3vnv6yrWG31gGUZrjq1c5pMmok5kDMLqEpYs1wFezv50PJTufmW2NEatM0A2bkMcVL3VilDe9MmX6CSCEFAbvn0iD0gDtNeSwpx5D6Xq7ZbYB8btQ_fXbSi-JDXSItF0Vux3ydId8RHAS-awAUxjskV4qOAMbtpcJjBRlHYvEokB_K5iOr_wW9PD1b5YhQpF0lYI1uhbdTLIUkmNn6-0pfPsMxiKVPIi8w5yhvOD4vD9WIWD1nHzy3WV4Iayls8yPcCbe8iWoeeBlA1BmkCi6MEMw8vYs6W_PeXfQiBL5JermOwhsw0AyUp80hFBqIhoNDOYif94-9S21_yYk3RY6RRc_gF-jvyDpeAE56QxSQDIdiZ5ieX3LgSVah7hEaa4t3CtpoWpi5qZCNR0-5GuiHG8UHQsMPO7UxtjncfkZNEkpQ2bhR-Hy86-QPgxcfBbfzdGGl5AnLLj3qy48H6jnQhtCEveG3p-g-Caf8yf1KI6rvitbKCc702YxkXaQO0OJHi1q9okicbuX_8SYP8i-ME8=s1360)
# Tautan


# Client Request Flow in Django

Berikut bagan alur request dari client sampai menghasilkan response pada aplikasi Django:
```mermaid
flowchart TD
    A[Client / Browser] --> B[urls.py]
    B --> C[views.py]
    C -->|Query/Save Data| D[models.py]
    C --> E[HTML Template (main.html)]
    D --> C
    E --> F[Response HTML]
    F --> A
``` 
![Diagram Alir](https://lh3.googleusercontent.com/d/1LtkKQ0I8GUUTb8_hC4mt8u2BJP5aPuc1=s1360)

### Penjelasan:
- **urls.py**: menentukan rute request, misalnya path `/` diarahkan ke fungsi `show_main` di `views.py`.  
- **views.py**: berisi fungsi yang memproses request; dapat mengakses `models.py` untuk mengambil/menyimpan data, lalu merender template.  
- **models.py**: berisi class Python yang mewakili tabel database; digunakan views untuk berinteraksi dengan data. Django secara otomatis membuat migration dengan ORM bawaannya.
- **HTML Template (main.html)**: berisi tampilan akhir yang akan diberikan sebagai response ke client, dengan placeholder yang akan dirender oleh views dan mengisi value mapping.  

# Peran `settings.py` dalam proyek Django
Berkas `settings.py` adalah konfigurasi dari sebuah proyek Django. Semua pengaturan penting didefinisikan di sini, seperti:
- **Database**: jenis database yang dipakai (SQLite, PostgreSQL, dll.), credential, dan lokasi.
- **INSTALLED_APPS**: daftar aplikasi Django (built-in maupun buatan kita) yang aktif dalam proyek.
- **Middleware**: komponen yang memproses request/response sebelum sampai ke views atau setelah keluar dari views.
- **Static & Media Files**: konfigurasi lokasi file statis (CSS, JS, gambar) dan file media (upload user).
- **Security**: pengaturan `SECRET_KEY`, `DEBUG`, dan `ALLOWED_HOSTS`.

# Cara kerja migrasi database di Django
Mekanisme migrasi di Django terdiri dari dua langkah:
1. **`makemigrations`** → Ketika kita membuat atau mengubah sebuah model di models.py, Django tidak langsung mengubah struktur database. Django terlebih dahulu membandingkan definisi model terbaru dengan kondisi terakhir yang sudah terekam (riwayat migrasi di tabel khusus (`django_migrations`)). Perubahan yang terdeteksi kemudian diterjemahkan ke dalam sebuah file migrasi saat kita menjalankan perintah makemigrations.
2. **`migrate`** → Di tahap ini, Django membaca semua file migrasi yang belum dijalankan (dicatat dalam tabel khusus bernama django_migrations di database). Kemudian Django menerjemahkan instruksi Python dalam file migrasi menjadi perintah SQL yang sesuai dengan jenis database yang digunakan (misalnya SQLite, PostgreSQL, atau MySQL). 

Dengan ini, Django juga dapat disebut memiliki ORM bawaan.

# Mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
Django dijadikan permulaan pembelajaran pengembangan perangkat lunak karena sifatnya yang lengkap, terstruktur, dan ramah pemula. Framework ini menganut prinsip "batteries included", artinya Django menyediakan banyak fitur bawaan yang siap dipakai, mulai dari ORM (Object-Relational Mapping), sistem autentikasi pengguna, hingga admin panel untuk mengelola data tanpa perlu menulis kode tambahan.

Alasan lain adalah karena di Fasilkom, mahasiswa sebelumnya sudah mengenal Python melalui mata kuliah DDP 1. Hal ini membuat transisi ke Django menjadi lebih mudah, karena Django sendiri ditulis menggunakan Python. Dengan begitu, mahasiswa tidak perlu mempelajari bahasa pemrograman baru sekaligus framework baru—cukup fokus pada konsep pengembangan perangkat lunak berbasis web.

Sebagai seorang developer, saya juga merasakan bahwa Django sangat cocok dijadikan framework pertama. Django membantu memahami alur pengembangan perangkat lunak dari ujung ke ujung: bagaimana request diproses oleh urls.py, ditangani oleh views.py, data dikelola oleh models.py, dan hasil akhirnya ditampilkan ke pengguna melalui template HTML. Ditambah lagi, ORM bawaan Django memudahkan pengelolaan database tanpa harus menulis SQL secara manual.

Dengan fitur-fitur tersebut, Django memberi gambaran yang jelas tentang praktik terbaik dalam membangun aplikasi perangkat lunak modern, dan struktur Django yang fixed juga membantu mahasiswa untuk on-track dalam organisasi sistem.

# Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
Sudah cukup baik.