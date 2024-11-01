from django.apps import AppConfig

# 用来存放APP类，不需要修改，因为只有一个APP
class HustravaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HustRava_app'
