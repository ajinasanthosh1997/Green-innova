from .base import * 

DEBUG = config("DEBUG", default=False, cast=bool)

# poetry add psycopg2-binary
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  
#         'NAME': config("DATABASE_NAME"),                     
#         'USER': config("DATABASE_USER"),                     
#         'PASSWORD': config("DATABASE_PASSWORD"),             
#         'HOST': 'localhost',                       
#         'PORT': '5432',                             
#     }
# }