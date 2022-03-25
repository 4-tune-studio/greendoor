MY_SECRET = {"SECRET_KEY": "m2y69wp0yx/3Zjs4IRCLERG2YcNGisc/Djl5TJua"}

MY_DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "gd-db",
        "USER": "fourtune",
        "PASSWORD": "greendoor4tune2wh",
        "HOST": "gd-db.cyt5fnsjiaht.ap-northeast-2.rds.amazonaws.com",
        "PORT": "3306",
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
        #     'charset': 'utf8mb4',
        #     "autocommit": True,
        # }
    }
}
