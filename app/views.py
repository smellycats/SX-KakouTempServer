# -*- coding: utf-8 -*-
import json
from functools import wraps
import shutil
import random

import arrow
import requests
from flask import g, request, make_response, jsonify, abort
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import func

from . import db, app, auth, cache, limiter, logger, access_logger
from models import *
#from help_func import *
import helper
import helper_kakou


def verify_addr(f):
    """IP地址白名单"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config['WHITE_LIST_OPEN'] or \
           request.remote_addr in set(['127.0.0.1', 'localhost']) or \
           request.remote_addr in app.config['WHITE_LIST']:
            pass
        else:
            return jsonify({
                'status': '403.6',
                'message': u'禁止访问:客户端的 IP 地址被拒绝'}), 403
        return f(*args, **kwargs)
    return decorated_function


@auth.verify_password
def verify_pw(username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        g.uid = user.id
        g.scope = set(user.scope.split(','))
        return sha256_crypt.verify(password, user.password)
    return False


def verify_scope(scope):
    def scope(f):
        """权限范围验证装饰器"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'all' in g.scope or scope in g.scope:
                return f(*args, **kwargs)
            else:
                abort(405)
        return decorated_function
    return scope


@app.route('/')
@limiter.limit("5000/hour")
def index_get():
    result = {
        'user_url': '%suser{/user_id}' % (request.url_root),
        'scope_url': '%sscope' % (request.url_root),
        'hcq1_url': '%skakou/hcq1' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header
    

@app.route('/user/<int:user_id>', methods=['GET'])
@limiter.limit('5000/hour')
@auth.login_required
def user_get(user_id):
    user = Users.query.filter_by(id=user_id, banned=0).first()
    if user is None:
        abort(404)
    result = {
        'id': user.id,
        'username': user.username,
        'scope': user.scope,
        'date_created': user.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        'date_modified': user.date_modified.strftime('%Y-%m-%d %H:%M:%S'),
        'banned': user.banned
    }
    return jsonify(result), 200


@app.route('/user', methods=['GET'])
@limiter.limit('5000/hour')
@auth.login_required
def user_list_get():
    try:
        limit = int(request.args.get('per_page', 20))
        offset = (int(request.args.get('page', 1)) - 1) * limit
        s = db.session.query(Users)
        q = request.args.get('q', None)
        if q is not None:
            s = s.filter(Users.username.like("%{0}%".format(q)))
        user = s.limit(limit).offset(offset).all()
        total = s.count()
        items = []
        for i in user:
            items.append({
                'id': i.id,
                'username': i.username,
                'scope': i.scope,
                'date_created': i.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                'date_modified': i.date_modified.strftime('%Y-%m-%d %H:%M:%S'),
                'banned': i.banned})
    except Exception as e:
        logger.exception(e)
    return jsonify({'total_count': total, 'items': items}), 200


@app.route('/user/<int:user_id>', methods=['POST', 'PUT'])
@limiter.limit('5000/hour')
@auth.login_required
def user_put(user_id):
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    if request.json.get('scope', None) is not None:
        # 所有权限范围
        all_scope = set()
        for i in Scope.query.all():
            all_scope.add(i.name)
        # 授予的权限范围
        request_scope = set(request.json.get('scope', u'null').split(','))
        # 求交集后的权限
        u_scope = ','.join(all_scope & request_scope)
        user.scope = u_scope
    if request.json.get('password', None) is not None:
        user.password = sha256_crypt.encrypt(
            request.json['password'], rounds=app.config['ROUNDS'])
    if request.json.get('banned', None) is not None:
        user.banned = request.json['banned']
    user.date_modified = arrow.now('PRC').datetime.replace(tzinfo=None)
    db.session.commit()

    return jsonify(), 204


@app.route('/user', methods=['POST'])
@limiter.limit('5000/hour')
@auth.login_required
def user_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    if not request.json.get('username', None):
        error = {
            'resource': 'user',
            'field': 'username',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if not request.json.get('password', None):
        error = {
            'resource': 'user',
            'field': 'password',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    if not request.json.get('scope', None):
        error = {
            'resource': 'user',
            'field': 'scope',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    
    user = Users.query.filter_by(username=request.json['username'],
                                 banned=0).first()
    if user:
        return jsonify({'message': 'username is already esist'}), 422

    password_hash = sha256_crypt.encrypt(
        request.json['password'], rounds=app.config['ROUNDS'])
    # 所有权限范围
    all_scope = set()
    for i in Scope.query.all():
        all_scope.add(i.name)
    # 授予的权限范围
    request_scope = set(request.json.get('scope', u'null').split(','))
    # 求交集后的权限
    u_scope = ','.join(all_scope & request_scope)
    t = arrow.now('PRC').datetime.replace(tzinfo=None)
    u = Users(username=request.json['username'], password=password_hash,
              date_created=t, date_modified=t, scope=u_scope, banned=0)
    db.session.add(u)
    db.session.commit()
    result = {
        'id': u.id,
        'username': u.username,
        'scope': u.scope,
        'date_created': u.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        'date_modified': u.date_modified.strftime('%Y-%m-%d %H:%M:%S'),
        'banned': u.banned
    }
    return jsonify(result), 201


@app.route('/scope', methods=['GET'])
@limiter.limit('5000/hour')
def scope_get():
    items = map(helper.row2dict, Scope.query.all())
    return jsonify({'total_count': len(items), 'items': items}), 200


@app.route('/temp/<string:city>', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def temp_post(city):
    model_dict = {
        'hcq': random.choice([TempHCQ1(), TempHCQ2(), TempHCQ3()]),
        'dyw': TempDYW(),
        'hy': TempHY(),
        'hd': TempHD(),
        'zk': TempZK(),
        'lm': TempLM(),
        'bl': TempBL()
    }
    if not city in model_dict.keys():
        abort(405)
    try:
        for i in request.json:
            t = model_dict[city]
            t.cltx_id = i['id']
            t.hphm = i['hphm']
            t.jgsj = i['jgsj']
            t.hpys = i['hpys']
            t.hpys_id = i['hpys_id']
            t.hpys_code = i['hpys_code']
            t.kkdd = i['kkdd']
            t.kkdd_id = i['kkdd_id']
            t.fxbh = i['fxbh']
            t.fxbh_code = i['fxbh_code']
            t.cdbh = i['cdbh']
            t.clsd = i['clsd']
            t.hpzl = i['hpzl']
            t.kkbh = ''
            t.clbj = i['clbj']
            t.imgurl = i['imgurl']
            t.flag = 0
            t.banned = 0
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.exception(e)


@app.route('/final/<string:city>', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def final_post(city):
    model_dict = {
        'hcq': FinalHCQ(),
        'dyw': FinalDYW(),
        'hy': FinalHY(),
        'hd': FinalHD(),
        'zk': FinalZK(),
        'lm': FinalLM(),
        'bl': FinalBL()
    }
    if not city in model_dict.keys():
        abort(405)
    try:
        for i in request.json:
            t = model_dict[city]
            t.cltx_id = i['id']
            t.hphm = i['hphm']
            t.jgsj = i['jgsj']
            t.hpys = i['hpys']
            t.hpys_id = i['hpys_id']
            t.hpys_code = i['hpys_code']
            t.kkdd = i['kkdd']
            t.kkdd_id = i['kkdd_id']
            t.fxbh = i['fxbh']
            t.fxbh_code = i['fxbh_code']
            t.cdbh = i['cdbh']
            t.clsd = i['clsd']
            t.hpzl = i['hpzl']
            t.kkbh = ''
            t.clbj = i['clbj']
            t.imgurl = i['imgurl']
            t.imgpath = i['imgpath']
            t.flag = 0
            t.banned = 0
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.exception(e)


@app.route('/maxid/<string:city>', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def maxid_get(city):
    model_dict = {
        'hcq': FinalHCQ,
        'dyw': FinalDYW,
        'hy': FinalHY,
        'hd': FinalHD,
        'zk': FinalZK,
        'lm': FinalLM,
        'bl': FinalBL
    }
    if not city in model_dict.keys():
        abort(405)
    try:
        q = db.session.query(func.max(model_dict[city].id)).first()
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.exception(e)


@app.route('/temp/<string:city>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def temp_list_get(city):
    q = request.args.get('q', None)
    if q is None:
	abort(400)
    try:
	args = json.loads(q)
    except Exception as e:
	logger.error(e)
	abort(400)
    model_dict = {
        'hcq1': TempHCQ1,
        'hcq2': TempHCQ2,
        'hcq3': TempHCQ3,
        'dyw': TempDYW,
        'hy': TempHY,
        'hd': TempHD,
        'zk': TempZK,
        'lm': TempLM,
        'bl': TempBL
    }
    if not city in model_dict.keys():
        abort(405)
    try:
        s = db.session.query(model_dict[city])
	if args.get('startid', None) is not None:
	    s = s.filter(model_dict[city].id >= args['startid'])
	if args.get('endid', None) is not None:
            s = s.filter(model_dict[city].id <= args['endid'])

        if len(s.all())==0:
            return jsonify({'items': [], 'total_count': 0})
	items = []
        for i in s.all():
	    item = {
                'id': i.id,
                'cltx_id': i.cltx_id,
                'hphm': i.hphm,
                'jgsj': i.jgsj.strftime('%Y-%m-%d %H:%M:%S'),
                'hpys': i.hpys,
                'hpys_id': i.hpys_id,
                'hpys_code': i.hpys_code,
                'kkdd': i.kkdd,
                'kkdd_id': i.kkdd_id,
                'fxbh': i.fxbh,
                'fxbh_code': i.fxbh_code,
                'cdbh': i.cdbh,
                'clsd': i.clsd,
                'hpzl': i.hpzl,
                'kkbh': i.kkbh,
                'clbj': i.clbj,
                'imgurl': i.imgurl,
                'flag': i.flag
            }
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.exception(e)


@app.route('/final/<string:city>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def final_list_get(city):
    q = request.args.get('q', None)
    if q is None:
	abort(400)
    try:
	args = json.loads(q)
    except Exception as e:
	logger.error(e)
	abort(400)
    model_dict = {
        'hcq': (FinalHCQ, LogHCQ),
        'dyw': (FinalDYW, LogDYW),
        'hy': (FinalHY, LogHY),
        'hd': (FinalHD, LogHD),
        'zk': (FinalZK, LogZK),
        'lm': (FinalLM, LogLM),
        'bl': (FinalBL, LogBL)
    }
    if not city in model_dict.keys():
        abort(405)

    try:
        query = db.session.query(model_dict[city][0])
	if args.get('startid', None):
	    query = query.filter(model_dict[city][0].id >= args['startid'])
	if args.get('endid', None):
            query = query.filter(model_dict[city][0].id <= args['endid'])
        if len(query.all())==0:
            return jsonify({'items': [], 'total_count': 0})
	query2 = db.session.query(model_dict[city][1])
	if args.get('startid', None):
	    query2 = query2.filter(model_dict[city][1].final_id >= args['startid'])
	if args.get('endid', None):
            query2 = query2.filter(model_dict[city][1].final_id <= args['endid'])
	items = []
	if len(query.all()) == len(query2.all()):
            for i, j in zip(query.all(), query2.all()):
	        item = {
                    'id': i.id,
                    'cltx_id': i.cltx_id,
                    'hphm': i.hphm,
                    'jgsj': i.jgsj.strftime('%Y-%m-%d %H:%M:%S'),
                    'hpys': i.hpys,
                    'hpys_id': i.hpys_id,
                    'hpys_code': i.hpys_code,
                    'kkdd': i.kkdd,
                    'kkdd_id': i.kkdd_id,
                    'fxbh': i.fxbh,
                    'fxbh_code': i.fxbh_code,
                    'cdbh': i.cdbh,
                    'clsd': i.clsd,
                    'hpzl': i.hpzl,
                    'kkbh': i.kkbh,
                    'clbj': i.clbj,
                    'imgurl': i.imgurl,
                    'imgpath': i.imgpath,
		    'date_created': j.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                    'flag': i.flag
                }
	        items.append(item)
	else:
            for i in query.all():
	        item = {
                    'id': i.id,
                    'cltx_id': i.cltx_id,
                    'hphm': i.hphm,
                    'jgsj': i.jgsj.strftime('%Y-%m-%d %H:%M:%S'),
                    'hpys': i.hpys,
                    'hpys_id': i.hpys_id,
                    'hpys_code': i.hpys_code,
                    'kkdd': i.kkdd,
                    'kkdd_id': i.kkdd_id,
                    'fxbh': i.fxbh,
                    'fxbh_code': i.fxbh_code,
                    'cdbh': i.cdbh,
                    'clsd': i.clsd,
                    'hpzl': i.hpzl,
                    'kkbh': i.kkbh,
                    'clbj': i.clbj,
                    'imgurl': i.imgurl,
                    'imgpath': i.imgpath,
		    'date_created': None,
                    'flag': i.flag
                }
	        items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.exception(e)


