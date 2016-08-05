﻿# -*- coding: utf-8 -*-


class Config(object):
    # 密码 string
    SECRET_KEY = 'hellokitty'
    # 服务器名称
    HEADER_SERVER = 'SX-KakouTempServer'
    # 加密次数 int
    ROUNDS = 123456
    # token生存周期，默认2小时 int
    EXPIRES = 7200
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../kakou.db'
    # 数据库连接绑定 dict
    SQLALCHEMY_BINDS = {
        'kakou': 'mysql://kakou:kakou@10.47.222.50/kakou_ser'
    }
    # 连接池大小 int
    #SQLALCHEMY_POOL_SIZE = 5
    # 用户权限范围 dict
    SCOPE_USER = {}
    # 白名单启用 bool
    WHITE_LIST_OPEN = True
    # 白名单列表 set
    WHITE_LIST = set()
    
    FLAG_IP = {
	1: '10.47.223.152',
	2: '10.47.223.150',
	3: '10.47.223.149',
	4: '10.47.223.148',
	5: '10.47.223.146',
	6: '10.47.223.145'
    }



class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False


class Testing(Config):
    TESTING = True
