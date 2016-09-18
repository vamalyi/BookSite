# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.conf import Settings as ThumbnailSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v!hoc*um31g14-$w%noc;%=(o&-&qxk32sc2l)!ukmv84+f(_6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sitemaps',

    # MPTTModel and Tree views in django admin
    'mptt',
    'django_mptt_admin',

    # Ckeditor
    'ckeditor_uploader',
    'ckeditor',

    # Thumbnails engine
    'easy_thumbnails',
    'image_cropping',

    # Chained selects
    'smart_selects',

    # Admin reorder feature
    'admin_reorder',

    # Import-Export
    'import_export',

    'genericadmin',
    'crispy_forms',
    'widget_tweaks',
    # 'adminsortable2',

    # APPS
    'webaccount',
    'website',
    'webshop',
    'weblayout',
    'webshopcart',
    'webrating',
    'wishlist',
    'analytics',
    'news',
)

# if DEBUG:
#     INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'solid_i18n.middleware.SolidLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('django_stackoverflow_trace.DjangoStackoverTraceMiddleware',)
    # MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1', '193.239.255.196', '::1']
# DJANGO_STACKOVERFLOW_TRACE_SEARCH_SITE = "googlesearch"

ADMIN_REORDER = (

    {'app': 'weblayout', 'label': 'Настройки', 'models': (
        {'model': 'weblayout.Menu', 'label': 'Меню'},
        {'model': 'webshop.FastSearch', 'label': 'Слова для быстрого поиска'},
        {'model': 'weblayout.SystemElement', 'label': 'Системные элементы'},
        {'model': 'website.GlobalSettings', 'label': 'Настройки сайта'},
        # {'model': 'weblayout.Template', 'label': 'Шаблоны'},
    )},

    {'app': 'website', 'label': 'Статические элементы', 'models': (
        {'model': 'website.StaticPage', 'label': 'Статические страницы'},
        {'model': 'news.Post', 'label': 'Статьи'},
        {'model': 'website.Gallery', 'label': 'Галереи'},
        {'model': 'website.Banner', 'label': 'Банера'},
        # {'model': 'website.BannerImagePosition', 'label': 'Изображения банеров'},
        # {'model': 'website.GalleryImagePosition', 'label': 'Изображения галерей'},
    )},

    {'app': 'webshop', 'label': 'Магазин', 'models': (
        {'model': 'webshop.Category', 'label': 'Категории'},
        {'model': 'webshop.Product', 'label': 'Товары'},
        {'model': 'webshop.PreFilter', 'label': 'Префильтры'},
        {'model': 'webshop.Currency', 'label': 'Валюты'},
        {'model': 'webshop.Author', 'label': 'Авторы'},
        {'model': 'webshop.BookSeries', 'label': 'Серии'},
        {'model': 'webshop.Provider', 'label': 'Провайдеры'},
        {'model': 'webshop.SpecialProposition', 'label': 'Специальные предложения'},
        {'model': 'webshop.ProductTreeReview', 'label': 'Reviews'},
        {'model': 'webshop.ProductParameter', 'label': 'Параметры товаров'},
        # {'model': 'webshop.ProductParameterValue', 'label': 'Значания параметров товаров'},
        # {'model': 'webshop.ProductParameterAvailableValue', 'label': 'Возможные значения параметров'},
        # {'model': 'webshop.ProductImagePosition', 'label': 'Изображения товаров'},
        {'model': 'webshop.Sale', 'label': 'Скидки'},
        # {'model': 'webshop.Margin', 'label': 'Наценки'},
        {'model': 'webshop.DeliveryRule', 'label': 'Варианты доставки'}

    )},

    {'app': 'webshopcart', 'label': 'Заказы', 'models': (
        # {'model': 'webshopcart.ProductInCart', 'label': 'Заказанные товары'},
        {'model': 'webshopcart.ProductCart', 'label': 'Заказы'},
    )},

    # {'app': 'webrating', 'label': 'Отзывы о сайте', 'models': (
    #     {'model': 'webrating.Rating', 'label': 'Отзывы'},
    # )},

    'auth',
)

ROOT_URLCONF = 'frankie_web_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',

                'website.context_processors.sys_elements',
                # 'website.context_processors.manufacturers',
                'website.context_processors.basket_count',
                'website.context_processors.metadata',
                'search.context_processors.search_form',
                'webshop.context_processors.fast_search',
            ],
        },
    },
]

WSGI_APPLICATION = 'frankie_web_platform.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'books',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
}

TEST = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'test_books',
}

AUTHENTICATION_BACKENDS = (
    'webaccount.auth_backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'auth.User'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGES = (
    # ('ru', _('Russian')),
    ('uk', _('Ukrainian')),
    # ('en', _('English')),
)

LANGUAGE_CODE = 'uk'
DEFAULT_LANGUAGE = 'uk'

SOLID_I18N_DEFAULT_PREFIX_REDIRECT = True

LOCALE_PATHS = ('locale',)

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Uncomment this line to test custom static files in developer mode
STATICFILES_DIRS = ('static',)

STATIC_ROOT = 'public/static'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SESSION_SAVE_EVERY_REQUEST = True

COMPRESS_HTML = False

CKEDITOR_UPLOAD_PATH = "uploads"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'Link', 'Unlink', 'Anchor',
             '-', 'Format',
             '-', 'Maximize',
             '-', 'Table',
             '-', 'Image',
             '-', 'Source',
             '-', 'NumberedList', 'BulletedList'
             ],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Font', 'FontSize', 'TextColor',
             '-', 'Outdent', 'Indent',
             '-', 'HorizontalRule',
             '-', 'Blockquote'
             ]
        ],
        'height': 500,
        'width': '100%',
        'toolbarCanCollapse': False,
        'forcePasteAsPlainText': True,
        'allowedContent': True,
        'filebrowserBrowseUrl': '/ckeditor/browse/',
        'filebrowserUploadUrl': '/ckeditor/upload/'
    }
}
USE_DJANGO_JQUERY = True
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

MEDIA_ROOT = 'public/media/books'
MEDIA_URL = '/media/'

GALLERY_IMAGE_LARGE = '1300x500'
GALLERY_IMAGE_MEDIUM = '750x230'
GALLERY_IMAGE_SMALL = '62x44'

PRODUCT_IMAGE_LARGE = '800x800'
PRODUCT_IMAGE_MEDIUM = '400x400'
PRODUCT_IMAGE_SMALL = '250x250'

SIMILAR_PRODUCTS_NUM = 1

PRODUCT_ON_PAGE = 12
NEWS_ON_PAGE = 12
PROFILE_ORDERS_ON_PAGE = 10

SEND_FROM_EMAIL = 'books Новый заказ <shop@books.com>'

RECIPIENT_LIST_FEEDBACK = ['shop@books.com']
RECIPIENT_LIST_ADMIN = ['shop@books.com']
RECIPIENT_LIST_USER = ['shop@books.com']

THUMBNAIL_PROCESSORS = ('image_cropping.thumbnail_processors.crop_corners',) + ThumbnailSettings.THUMBNAIL_PROCESSORS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'ula.books@gmail.com'
EMAIL_HOST_PASSWORD = 'ssula2016'
EMAIL_USE_SSL = True

HOMEPAGE = '/'
SHOP_NAME = 'Books'

NOVA_POSHTA_KEY = 'f7d9972613b46d44cb879d1f2be8b1c8'

RECENTLY_VIEWED_COOKIE_NAME = 'product_history'
RECENTLY_VIEWED_PRODUCTS = 20
RECENTLY_VIEWED_COOKIE_LIFETIME = 14 * 24 * 60 * 60
RECENTLY_VIEWED_COOKIE_SECURE = False

COOKIES_DELETE_ON_LOGOUT = ['product_history']
MODERATE_REVIEWS = True
ALLOW_ANON_REVIEWS = True
