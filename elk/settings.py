from datetime import timedelta

import environ
from easy_thumbnails.conf import Settings as thumbnail_settings

from elk.context_processors import revision

root = environ.Path(__file__) - 3        # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env()                   # reading .env file

SITE_ROOT = root()

USE_L10N = True
USE_i18N = True
USE_TZ = True
TIME_ZONE = env('TIME_ZONE')

# LANGUAGE_CODE = "ru"

# default formats, used when localization is fully off, i.e. in outgoing emails
SHORT_DATE_FORMAT = 'D, M d'
SHORT_DATETIME_FORMAT = 'M d, h:i A'
TIME_FORMAT = 'h:i a'

FORMAT_MODULE_PATH = [
    'elk.formats'
]

DEBUG = env('DEBUG')    # False if not in os.environ

ALLOWED_HOSTS = [
    'a.elk.today',
    'a-staging.elk.today',
    '127.0.0.1',
]
ABSOLUTE_HOST = 'https://a.elk.today'

SUPPORT_EMAIL = 'help@elk.today'
REPLY_TO = 'help@elk.today'
SERVER_EMAIL = 'django@elk.today'
EMAIL_NOTIFICATIONS_FROM = env('EMAIL_NOTIFICATIONS_FROM')

ADMINS = [
    ('Fedor Borshev', 'f@f213.in'),
]

DATABASES = {
    'default': env.db(),    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
}

INSTALLED_APPS = [
    'elk',
    'crm',  # stuff related to student accounts
    'lessons',  # lesson types — Ordinary lessons, Native speaker lessons etc
    'products',  # staff that student can purchase, i.e. Subscription
    'market',   # lesson planning takes place here
    'timeline',  # teachers curricullom
    'teachers',  # teachers database
    'acc',   # acc — loggin in and out, homepage
    'history',  # an app for future data mining — all significant user actions are recorded here
    'mailer',
    'extevents',  # integrations with external calendars, like Google's one
    'manual_class_logging',  # temporary app to log classes completed outside the system. Should be deleted in 2016
    'accounting',  # teacher accounting — passed classes, customer inspired cancellation etc
    'payments',  # students payment processing

    'easy_thumbnails',
    'image_cropping',
    'djmoney',
    'anymail',
    'mail_templated',
    'django_countries',
    'django_markdown',
    'django_user_agents',
    'social.apps.django_app.default',
    'timezone_field',
    'django_nose',
    'django.contrib.admindocs',
    'suit',
    'date_range_filter',
    'raven.contrib.django.raven_compat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'elk.middleware.GuessCountryMiddleWare',
    'elk.middleware.TimezoneMiddleware',
    'elk.middleware.SaveRefMiddleWare',
    'elk.middleware.MarkTrialMiddleWare',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--nologcapture'
]

ROOT_URLCONF = 'elk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.tz',

                'elk.context_processors.support_email',  # support email address configured in .env
                'elk.context_processors.revision',  # git revision for frontend

                'elk.context_processors.greeting',  # current customer greeting template

                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',

            ],
        },
    },
]

SUIT_CONFIG = {
    'ADMIN_NAME': 'ELK back-office',
    'MENU': (
        {'app': 'accounting', 'icon': 'icon-gift', },
        {'app': 'crm', 'icon': 'icon-globe', 'models': ('crm.Customer', 'crm.Company')},
        {'app': 'market', 'icon': 'icon-shopping-cart', 'models': ('market.Subscription', 'market.Class')},
        {'app': 'teachers', 'icon': 'icon-briefcase', },
        {'app': 'lessons', 'icon': 'icon-headphones', 'label': 'Teaching', 'models': ('lessons.Language', 'lessons.PairedLesson', 'lessons.MasterClass', 'lessons.HappyHour')},
        {'app': 'products', 'icon': 'icon-list', 'label': 'Products'},
        {'app': 'auth', 'label': 'Authorization', 'icon': 'icon-lock', 'models': ('auth.User', 'auth.Group')},
    ),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
)
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'acc.pipelines.save_profile_picture',
    'acc.pipelines.save_country',
    'acc.pipelines.save_timezone',
    'acc.pipelines.save_referral',
    'acc.pipelines.add_trial_lesson',
    'acc.pipelines.notify_staff',
)

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/vendor/jquery/dist/jquery.min.js',
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',

    # profiling blocks admin login on the test machine. If you need it — uncomment
    # 'debug_toolbar.panels.profiling.ProfilingPanel',
    #
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INTERNAL_IPS = [
    '127.0.0.1',
    '::1',
    '77.37.209.221',
    '91.197.114.155',
    '91.197.113.166',
]

if not DEBUG:
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'sentry': {
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'release': revision(None),
            },
        },
        'loggers': {
            'app': {
                'level': 'DEBUG',
                'handlers': ['sentry'],
            },
        },
    }

SOCIAL_AUTH_URL_NAMESPACE = 'acc:social'

SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, first_name, last_name, email'
}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


GROOVE_API_TOKEN = env('GROOVE_API_TOKEN')

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

WSGI_APPLICATION = 'elk.wsgi.application'

public_root = root.path('public/')

MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')

STATIC_URL = env('STATIC_URL')
STATIC_ROOT = env('STATIC_ROOT')

SECRET_KEY = env('SECRET_KEY')  # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
ANYMAIL = {
    'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_SENDER_DOMAIN')
}
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_ASYNC = env.bool('EMAIL_ASYNC')

CACHES = {
    'default': env.cache(),
}

BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

CELERYBEAT_SCHEDULE = {
    'check_classes_that_will_start_soon': {
        'task': 'timeline.tasks.notify_15min_to_class',
        'schedule': timedelta(minutes=1),
    },
    'update_google_calendars': {
        'task': 'extevents.tasks.update_google_calendars',
        'schedule': timedelta(minutes=5),
    },
    'bill_timeline_entries': {
        'task': 'accounting.tasks.bill_timeline_entries',
        'schedule': timedelta(minutes=1),
    },
}


CELERY_TIMEZONE = env('TIME_ZONE')

GEOIP_PATH = './geolite/'

STRIPE_API_KEY = '***REMOVED***'
STRIPE_PK = '***REMOVED***'

# Uncomment this lines to catch all runtime warnings as errors

# import warnings  # noqa
# warnings.filterwarnings(
#     'error', r".*",
#     RuntimeWarning, r".*"
# )
