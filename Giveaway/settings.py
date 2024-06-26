from pathlib import Path
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.environ.get("SECRET_KEY", "some value if your key is not in the environment")
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = config('DEBUG', cast=bool)
DEBUG = False

ALLOWED_HOSTS = ['www.dashme.ng']


# Application definition
SOCIALACCOUNT_PROVIDERS={
    'google':{
        'SCOPE':[
            'profile',
            'email',
        ],
        'AUTH_PARAMS':{
            'access_type':'online',
        }
    }
}





INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'givers',
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'social_django',
    #'givers.apps.GiversConfig',

]

AUTHENTICATION_BACKENDS=(
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.google.GoogleOAuth2',

)

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'givers.middleware.AutoLogout',


]

ROOT_URLCONF = 'Giveaway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

            ],
        },
    },
]

WSGI_APPLICATION = 'Giveaway.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresdb',
        'USER': 'shawen17',
        'PASSWORD': 'Shawenpogres',
        'HOST': 'shawen17-2443.postgres.pythonanywhere-services.com',
        'PORT':12443,
    }
}

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/shawen17/Giveaway/db.sqlite3',
    }
}'''


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'givers/static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

LOGIN_URL='/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = 'user_account'
LOGOUT_REDIRECT_URL = 'home'


SESSION_EXPIRE_SECONDS = 240

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


AUTO_LOGOUT_DELAY = 10

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

EMAIL_USE_SSL= True
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'mail.dashme.ng'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


#payment solution sample
PAYTM_MERCHANT_ID = '<your_merchant_id>'
PAYTM_SECRET_KEY = '<your_paytm_secret_key>'
PAYTM_WEBSITE = 'WEBSTAGING'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'

#google recaptcha
GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get("GOOGLE_RECAPTCHA_SITE_KEY")

GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get("GOOGLE_RECAPTCHA_SECRET_KEY")

#twitter
SOCIAL_AUTH_TWITTER_KEY= os.environ.get("SOCIAL_AUTH_TWITTER_KEY")
SOCIAL_AUTH_TWITTER_SECRET= os.environ.get("SOCIAL_AUTH_TWITTER_SECRET")

#facebook
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]

SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET= True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True

DJANGORESIZED_DEFAULT_SIZE = [500,500]
DJANGORESIZED_DEFAULT_QUALITY = 90
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
