# -*- coding: utf-8 -*-
import json
from functools import wraps
import shutil
import cStringIO

import arrow
import requests
from flask import g, request, make_response, jsonify, abort
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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


def verify_token(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if app.config['TOKEN_OPEN']:
            g.uid = helper.ip2num(request.remote_addr)
            g.scope = set(['all'])
        else:
            if not request.headers.get('Access-Token'):
                return jsonify({'status': '401.6',
                                'message': 'missing token header'}), 401
            token_result = verify_auth_token(request.headers['Access-Token'],
                                             app.config['SECRET_KEY'])
            if not token_result:
                return jsonify({'status': '401.7',
                                'message': 'invalid token'}), 401
            elif token_result == 'expired':
                return jsonify({'status': '401.8',
                                'message': 'token expired'}), 401
            g.uid = token_result['uid']
            g.scope = set(token_result['scope'])

        return f(*args, **kwargs)
    return decorated_function


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
#@auth.login_required
def index_get():
    result = {
        'user_url': 'http://%suser{/user_id}' % (request.url_root),
        'scope_url': 'http://%sscope' % (request.url_root),
        'hcq1_url': 'http://%skakou/hcq1' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header
    

@app.route('/user', methods=['OPTIONS'])
@limiter.limit('5000/hour')
def user_options():
    return jsonify(), 200

@app.route('/user/<int:user_id>', methods=['GET'])
@limiter.limit('5000/hour')
@auth.login_required
def user_get(user_id):
    user = Users.query.filter_by(id=user_id, banned=0).first()
    if user:
        result = {
            'id': user.id,
            'username': user.username,
            'scope': user.scope,
            'date_created': str(user.date_created),
            'date_modified': str(user.date_modified),
            'banned': user.banned
        }
        return jsonify(result), 200
    else:
        abort(404)

@app.route('/user/<int:user_id>', methods=['POST', 'PATCH'])
@limiter.limit('5000/hour')
@auth.login_required
def user_patch(user_id):
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    if not request.json.get('scope', None):
        error = {
            'resource': 'user',
            'field': 'scope',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    # 所有权限范围
    all_scope = set()
    for i in Scope.query.all():
        all_scope.add(i.name)
    # 授予的权限范围
    request_scope = set(request.json.get('scope', u'null').split(','))
    # 求交集后的权限
    u_scope = ','.join(all_scope & request_scope)

    db.session.query(Users).filter_by(id=user_id).update(
        {'scope': u_scope, 'date_modified': arrow.now().datetime})
    db.session.commit()

    user = Users.query.filter_by(id=user_id).first()

    return jsonify({
        'id': user.id,
        'username': user.username,
        'scope': user.scope,
        'date_created': str(user.date_created),
        'date_modified': str(user.date_modified),
        'banned': user.banned
    }), 201

@app.route('/user', methods=['POST'])
@limiter.limit('5000/hour')
#@auth.login_required
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
    print password_hash
    return
    # 所有权限范围
    all_scope = set()
    for i in Scope.query.all():
        all_scope.add(i.name)
    # 授予的权限范围
    request_scope = set(request.json.get('scope', u'null').split(','))
    # 求交集后的权限
    u_scope = ','.join(all_scope & request_scope)
    u = Users(username=request.json['username'], password=password_hash,
              scope=u_scope, banned=0)
    db.session.add(u)
    db.session.commit()
    result = {
        'id': u.id,
        'username': u.username,
        'scope': u.scope,
        'date_created': str(u.date_created),
        'date_modified': str(u.date_modified),
        'banned': u.banned
    }
    return jsonify(result), 201

@app.route('/scope', methods=['OPTIONS'])
@limiter.limit('5000/hour')
def scope_options():
    return jsonify(), 200

@app.route('/scope', methods=['GET'])
@limiter.limit('5000/hour')
def scope_get():
    items = map(helper.row2dict, Scope.query.all())
    return jsonify({'total_count': len(items), 'items': items}), 200

    
@app.route('/token', methods=['OPTIONS'])
@limiter.limit('5000/hour')
def token_options():
    return jsonify(), 200

@app.route('/token', methods=['POST'])
@limiter.limit('5/minute')
def token_post():
    try:
        if request.json is None:
            return jsonify({'message': 'Problems parsing JSON'}), 415
        if not request.json.get('username', None):
            error = {
                'resource': 'Token',
                'field': 'username',
                'code': 'missing_field'
            }
            return jsonify({'message': 'Validation Failed', 'errors': error}), 422
        if not request.json.get('password', None):
            error = {'resource': 'Token', 'field': 'password',
                     'code': 'missing_field'}
            return jsonify({'message': 'Validation Failed', 'errors': error}), 422
        user = Users.query.filter_by(username=request.json.get('username'),
                                     banned=0).first()
        if not user:
            return jsonify({'message': 'username or password error'}), 422
        if not sha256_crypt.verify(request.json.get('password'), user.password):
            return jsonify({'message': 'username or password error'}), 422

        s = Serializer(app.config['SECRET_KEY'],
                       expires_in=app.config['EXPIRES'])
        token = s.dumps({'uid': user.id, 'scope': user.scope.split(',')})
    except Exception as e:
        print e

    return jsonify({
        'uid': user.id,
        'access_token': token,
        'token_type': 'self',
        'scope': user.scope,
        'expires_in': app.config['EXPIRES']
    }), 201


@app.route('/kakou/hcq1', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hcq1_post():
    try:
        for i in request.json:
            t = TempHCQ1(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                         hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                         kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		         cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
			 clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)


@app.route('/kakou/hcq2', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hcq2_post():
    try:
        for i in request.json:
            t = TempHCQ2(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                         hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                         kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		         cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
			 clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)

@app.route('/kakou/hcq3', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hcq3_post():
    try:
        for i in request.json:
            t = TempHCQ3(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                         hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                         kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		         cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
			 clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)

@app.route('/kakou/dyw', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def dyw_post():
    try:
        for i in request.json:
            t = TempDYW(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                        hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                        kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		        cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
			clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)


@app.route('/kakou/hy', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hy_post():
    try:
        for i in request.json:
            t = TempHY(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                       hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                       kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		       cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
		       clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)


@app.route('/kakou/hd', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hd_post():
    try:
        for i in request.json:
            t = TempHD(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                       hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                       kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		       cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh=i['kkbh'],
		       clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)


@app.route('/kakou/zk', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def zk_post():
    try:
        for i in request.json:
            t = TempZK(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                       hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                       kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		       cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
		       clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)


@app.route('/kakou/lm', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def lm_post():
    try:
        for i in request.json:
            t = TempLM(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                       hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                       kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		       cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
		       clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.error(e)


@app.route('/kakou/bl', methods=['POST'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def bl_post():
    try:
        for i in request.json:
            t = TempBL(cltx_id=i['id'], hphm=i['hphm'], jgsj=i['jgsj'], hpys=i['hpys'],
                       hpys_id=i['hpys_id'], hpys_code=i['hpys_code'], kkdd=i['kkdd'],
                       kkdd_id=i['kkdd_id'], fxbh=i['fxbh'], fxbh_code=i['fxbh_code'],
		       cdbh=i['cdbh'], clsd=i['clsd'], hpzl=i['hpzl'], kkbh='',
		       clbj=i['clbj'], imgurl=i['imgurl'], flag=0, banned=0)
            db.session.add(t)
    	db.session.commit()
        
	return jsonify({'total': len(request.json)}), 201
    except Exception as e:
	logger.exception(e)


@app.route('/maxid/hcq', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hcq_maxid_get():
    try:
        sql = ("select max(id) from final_hcq")
        q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
        
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.error(e)

@app.route('/maxid/dyw', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def dyw_maxid_get():
    try:
        sql = ("select max(id) from final_dyw")
        q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
        
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.error(e)


@app.route('/maxid/hy', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hy_maxid_get():
    try:
        sql = ("select max(id) from final_hy")
        q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
        
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.error(e)


@app.route('/maxid/hd', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def hd_maxid_get():
    try:
        sql = ("select max(id) from final_hd")
        q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
        
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.error(e)


@app.route('/maxid/zk', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def zk_maxid_get():
    try:
        sql = ("select max(id) from final_zk")
        q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
        
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.error(e)


@app.route('/maxid/lm', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def lm_maxid_get():
    try:
        sql = ("select max(id) from final_lm")
        q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
        
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.error(e)


@app.route('/maxid/bl', methods=['GET'])
@limiter.limit('5000/minute')
#@limiter.exempt
#@auth.login_required
def bl_maxid_get():
    try:
        sql = ("select max(id) from final_bl")
        q = db.get_engine(app, bind='kakou').execute(sql).fetchone()
        
	return jsonify({'maxid': q[0]}), 200
    except Exception as e:
	logger.error(e)


@app.route('/final/hcq/<int:start_id>/<int:end_id>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def hcq_final_get(start_id, end_id):
    try:
	items = []
	sql = ("select f.*, l.date_created from final_hcq as f left join log_hcq as l on f.id = l.final_id where f.id >= {0} and f.id <= {1}".format(start_id, end_id))
        q = db.get_engine(app, bind='kakou').execute(sql).fetchall()
        for i in q:
	    item = {}
	    item['id'] = i[0]
	    item['cltx_id'] = i[1]
	    item['hphm'] = i[2]
	    item['jgsj'] = str(i[3])
	    item['hpys'] = i[4]
	    item['hpys_id'] = i[5]
	    item['hpys_code'] = i[6]
	    item['kkdd'] = i[7]
	    item['kkdd_id'] = i[8]
	    item['fxbh'] = i[9]
	    item['fxbh_code'] = i[10]
	    item['cdbh'] = i[11]
	    item['clsd'] = i[12]
            item['hpzl'] = i[13]
	    item['kkbh'] = i[14]
	    item['clbj'] = i[15]
	    item['imgurl'] = 'http://%s:8090/' % app.config['FLAG_IP'].get(i[18], '10.47.223.148')+i[17].replace('\\', '/')
	    item['date_created'] = str(i[20])
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.error(e)


@app.route('/final/dyw/<int:start_id>/<int:end_id>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def dyw_final_get(start_id, end_id):
    try:
	items = []
	sql = ("select f.*, l.date_created from final_dyw as f left join log_dyw as l on f.id = l.final_id where f.id >= {0} and f.id <= {1}".format(start_id, end_id))
        q = db.get_engine(app, bind='kakou').execute(sql).fetchall()
        for i in q:
	    item = {}
	    item['id'] = i[0]
	    item['cltx_id'] = i[1]
	    item['hphm'] = i[2]
	    item['jgsj'] = str(i[3])
	    item['hpys'] = i[4]
	    item['hpys_id'] = i[5]
	    item['hpys_code'] = i[6]
	    item['kkdd'] = i[7]
	    item['kkdd_id'] = i[8]
	    item['fxbh'] = i[9]
	    item['fxbh_code'] = i[10]
	    item['cdbh'] = i[11]
	    item['clsd'] = i[12]
            item['hpzl'] = i[13]
	    item['kkbh'] = i[14]
	    item['clbj'] = i[15]
	    item['imgurl'] = 'http://%s:8090/' % app.config['FLAG_IP'].get(i[18], '10.47.223.150')+i[17].replace('\\', '/')
	    item['date_created'] = str(i[20])
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.error(e)


@app.route('/final/hy/<int:start_id>/<int:end_id>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def hy_final_get(start_id, end_id):
    try:
	items = []
	sql = ("select f.*, l.date_created from final_hy as f left join log_hy as l on f.id = l.final_id where f.id >= {0} and f.id <= {1}".format(start_id, end_id))
        q = db.get_engine(app, bind='kakou').execute(sql).fetchall()
        for i in q:
	    item = {}
	    item['id'] = i[0]
	    item['cltx_id'] = i[1]
	    item['hphm'] = i[2]
	    item['jgsj'] = str(i[3])
	    item['hpys'] = i[4]
	    item['hpys_id'] = i[5]
	    item['hpys_code'] = i[6]
	    item['kkdd'] = i[7]
	    item['kkdd_id'] = i[8]
	    item['fxbh'] = i[9]
	    item['fxbh_code'] = i[10]
	    item['cdbh'] = i[11]
	    item['clsd'] = i[12]
            item['hpzl'] = i[13]
	    item['kkbh'] = i[14]
	    item['clbj'] = i[15]
	    item['imgurl'] = 'http://%s:8090/' % app.config['FLAG_IP'].get(i[18], '10.47.223.152')+i[17].replace('\\', '/')
	    item['date_created'] = str(i[20])
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.error(e)


@app.route('/final/hd/<int:start_id>/<int:end_id>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def hd_final_get(start_id, end_id):
    try:
	items = []
	sql = ("select f.*, l.date_created from final_hd as f left join log_hd as l on f.id = l.final_id where f.id >= {0} and f.id <= {1}".format(start_id, end_id))
        q = db.get_engine(app, bind='kakou').execute(sql).fetchall()
        for i in q:
	    item = {}
	    item['id'] = i[0]
	    item['cltx_id'] = i[1]
	    item['hphm'] = i[2]
	    item['jgsj'] = str(i[3])
	    item['hpys'] = i[4]
	    item['hpys_id'] = i[5]
	    item['hpys_code'] = i[6]
	    item['kkdd'] = i[7]
	    item['kkdd_id'] = i[8]
	    item['fxbh'] = i[9]
	    item['fxbh_code'] = i[10]
	    item['cdbh'] = i[11]
	    item['clsd'] = i[12]
            item['hpzl'] = i[13]
	    item['kkbh'] = i[14]
	    item['clbj'] = i[15]
	    item['imgurl'] = 'http://%s:8090/' % app.config['FLAG_IP'].get(i[18], '10.47.223.149')+i[17].replace('\\', '/')
	    item['date_created'] = str(i[20])
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.error(e)


@app.route('/final/zk/<int:start_id>/<int:end_id>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def zk_final_get(start_id, end_id):
    try:
	items = []
	sql = ("select f.*, l.date_created from final_zk as f left join log_zk as l on f.id = l.final_id where f.id >= {0} and f.id <= {1}".format(start_id, end_id))
        q = db.get_engine(app, bind='kakou').execute(sql).fetchall()
        for i in q:
	    item = {}
	    item['id'] = i[0]
	    item['cltx_id'] = i[1]
	    item['hphm'] = i[2]
	    item['jgsj'] = str(i[3])
	    item['hpys'] = i[4]
	    item['hpys_id'] = i[5]
	    item['hpys_code'] = i[6]
	    item['kkdd'] = i[7]
	    item['kkdd_id'] = i[8]
	    item['fxbh'] = i[9]
	    item['fxbh_code'] = i[10]
	    item['cdbh'] = i[11]
	    item['clsd'] = i[12]
            item['hpzl'] = i[13]
	    item['kkbh'] = i[14]
	    item['clbj'] = i[15]
	    item['imgurl'] = 'http://%s:8090/' % app.config['FLAG_IP'].get(i[18], '10.47.223.152')+i[17].replace('\\', '/')
	    item['date_created'] = str(i[20])
	    items.append(item)
	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.error(e)


@app.route('/final/lm/<int:start_id>/<int:end_id>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def lm_final_get(start_id, end_id):
    try:
	items = []
	sql = ("select f.*, l.date_created from final_lm as f left join log_lm as l on f.id = l.final_id where f.id >= {0} and f.id <= {1}".format(start_id, end_id))
        q = db.get_engine(app, bind='kakou').execute(sql).fetchall()
        for i in q:
	    item = {}
	    item['id'] = i[0]
	    item['cltx_id'] = i[1]
	    item['hphm'] = i[2]
	    item['jgsj'] = str(i[3])
	    item['hpys'] = i[4]
	    item['hpys_id'] = i[5]
	    item['hpys_code'] = i[6]
	    item['kkdd'] = i[7]
	    item['kkdd_id'] = i[8]
	    item['fxbh'] = i[9]
	    item['fxbh_code'] = i[10]
	    item['cdbh'] = i[11]
	    item['clsd'] = i[12]
            item['hpzl'] = i[13]
	    item['kkbh'] = i[14]
	    item['clbj'] = i[15]
	    item['imgurl'] = 'http://%s:8090/' % app.config['FLAG_IP'].get(i[18], '10.47.223.149')+i[17].replace('\\', '/')
	    item['date_created'] = str(i[20])
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.error(e)


@app.route('/final/bl/<int:start_id>/<int:end_id>', methods=['GET'])
@limiter.limit('500/minute')
#@limiter.exempt
#@auth.login_required
def bl_final_get(start_id, end_id):
    try:
	items = []
	sql = ("select f.*, l.date_created from final_bl as f left join log_bl as l on f.id = l.final_id where f.id >= {0} and f.id <= {1}".format(start_id, end_id))
        q = db.get_engine(app, bind='kakou').execute(sql).fetchall()
        for i in q:
	    item = {}
	    item['id'] = i[0]
	    item['cltx_id'] = i[1]
	    item['hphm'] = i[2]
	    item['jgsj'] = str(i[3])
	    item['hpys'] = i[4]
	    item['hpys_id'] = i[5]
	    item['hpys_code'] = i[6]
	    item['kkdd'] = i[7]
	    item['kkdd_id'] = i[8]
	    item['fxbh'] = i[9]
	    item['fxbh_code'] = i[10]
	    item['cdbh'] = i[11]
	    item['clsd'] = i[12]
            item['hpzl'] = i[13]
	    item['kkbh'] = i[14]
	    item['clbj'] = i[15]
	    item['imgurl'] = 'http://%s:8090/' % app.config['FLAG_IP'].get(i[18], '10.47.223.149')+i[17].replace('\\', '/')
	    item['date_created'] = str(i[20])
	    items.append(item)

	return jsonify({'items': items, 'total_count': len(items)})
    except Exception as e:
	logger.error(e)