# -*- coding: utf-8 -*-
import arrow

from . import db


class Users(db.Model):
    """用户"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    password = db.Column(db.String(255))
    scope = db.Column(db.String(255), default='')
    date_created = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    date_modified = db.Column(
        db.DateTime, default=arrow.now('PRC').datetime.replace(tzinfo=None))
    banned = db.Column(db.Integer, default=0)

    def __init__(self, username, password, scope='', date_created=None,
                 date_modified=None, banned=0):
        self.username = username
        self.password = password
        self.scope = scope
        now = arrow.now('PRC').datetime.replace(tzinfo=None)
        if date_created is None:
            self.date_created = now
        else:
            self.date_created = date_created
        if date_modified is None:
            self.date_modified = now
        else:
            self.date_modified = date_modified
        self.banned = banned

    def __repr__(self):
        return '<Users %r>' % self.id


class Scope(db.Model):
    """权限范围"""
    __tablename__ = 'scope'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Scope %r>' % self.id


class BaseTemp(db.Model):
    """临时表"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    cltx_id = db.Column(db.Integer)
    hphm = db.Column(db.String(16))
    jgsj = db.Column(db.DateTime)
    hpys = db.Column(db.String(16))
    hpys_id = db.Column(db.Integer)
    hpys_code = db.Column(db.String(8))
    kkdd = db.Column(db.String(64))
    kkdd_id = db.Column(db.String(32))
    fxbh = db.Column(db.String(16))
    fxbh_code = db.Column(db.String(8))
    cdbh = db.Column(db.Integer)
    clsd = db.Column(db.Integer)
    hpzl = db.Column(db.String(8))
    kkbh = db.Column(db.String(64))
    clbj = db.Column(db.String(8))
    imgurl = db.Column(db.String(255))
    flag = db.Column(db.Integer)
    banned = db.Column(db.Integer)

    def __init__(self, cltx_id=0, hphm='-', jgsj=None, hpys='', hpys_id=1,
                 hpys_code='', kkdd='', kkdd_id='', fxbh='', fxbh_code='',
                 cdbh=1, clsd=0, hpzl='', kkbh='', clbj='', imgurl='',
                 flag=0, banned=0):
        self.cltx_id = cltx_id
        self.hphm = hphm
        self.jgsj = jgsj
	self.hpys = hpys
	self.hpys_id = hpys_id
	self.hpys_code = hpys_code
	self.kkdd = kkdd
	self.kkdd_id = kkdd_id
	self.fxbh = fxbh
	self.fxbh_code = fxbh_code
	self.cdbh = cdbh
	self.clsd = clsd
	self.hpzl = hpzl
	self.kkbh = kkbh
	self.clbj = clbj
	self.imgurl = imgurl
	self.flag = flag
	self.banned = banned

    def __repr__(self):
        return '<BaseTemp %r>' % self.id


class TempHCQ1(BaseTemp):
    __tablename__ = 'temp_hcq1'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempHCQ1 %r>' % self.id


class TempHCQ2(BaseTemp):
    __tablename__ = 'temp_hcq2'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempHCQ2 %r>' % self.id


class TempHCQ3(BaseTemp):
    __tablename__ = 'temp_hcq3'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempHCQ3 %r>' % self.id


class TempDYW(BaseTemp):
    __tablename__ = 'temp_dyw'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempDYW %r>' % self.id


class TempHY(BaseTemp):
    __tablename__ = 'temp_hy'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempHY %r>' % self.id


class TempHD(BaseTemp):
    __tablename__ = 'temp_hd'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempHD %r>' % self.id


class TempZK(BaseTemp):
    __tablename__ = 'temp_zk'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempZK %r>' % self.id


class TempLM(BaseTemp):
    __tablename__ = 'temp_lm'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempLM %r>' % self.id


class TempBL(BaseTemp):
    __tablename__ = 'temp_bl'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<TempBL %r>' % self.id


class BaseFinal(db.Model):
    """基础表"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    cltx_id = db.Column(db.Integer)
    hphm = db.Column(db.String(16))
    jgsj = db.Column(db.DateTime)
    hpys = db.Column(db.String(16))
    hpys_id = db.Column(db.Integer)
    hpys_code = db.Column(db.String(8))
    kkdd = db.Column(db.String(64))
    kkdd_id = db.Column(db.String(32))
    fxbh = db.Column(db.String(16))
    fxbh_code = db.Column(db.String(8))
    cdbh = db.Column(db.Integer)
    clsd = db.Column(db.Integer)
    hpzl = db.Column(db.String(8))
    kkbh = db.Column(db.String(64))
    clbj = db.Column(db.String(8))
    imgurl = db.Column(db.String(255))
    imgpath = db.Column(db.String(255))
    flag = db.Column(db.Integer)
    banned = db.Column(db.Integer)

    def __init__(self, cltx_id=0, hphm='-', jgsj='', hpys='', hpys_id=1,
                 hpys_code='', kkdd='', kkdd_id='', fxbh='', fxbh_code='',
                 cdbh=1, clsd=0, hpzl='', kkbh='', clbj='', imgurl='',
                 imgpath='', flag=0, banned=0):
        self.cltx_id = cltx_id
        self.hphm = hphm
        self.jgsj = jgsj
	self.hpys = hpys
	self.hpys_id = hpys_id
	self.hpys_code = hpys_code
	self.kkdd = kkdd
	self.kkdd_id = kkdd_id
	self.fxbh = fxbh
	self.fxbh_code = fxbh_code
	self.cdbh = cdbh
	self.clsd = clsd
	self.hpzl = hpzl
	self.kkbh = kkbh
	self.clbj = clbj
	self.imgurl = imgurl
	self.imgpath = imgpath
	self.flag = flag
	self.banned = banned

    def __repr__(self):
        return '<BaseFinal %r>' % self.id


class FinalHCQ(BaseFinal):
    __tablename__ = 'final_hcq'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<FinalHCQ %r>' % self.id


class FinalDYW(BaseFinal):
    __tablename__ = 'final_dyw'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<FinalDYW %r>' % self.id


class FinalHY(BaseFinal):
    __tablename__ = 'final_hy'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<FinalHY %r>' % self.id


class FinalHD(BaseFinal):
    __tablename__ = 'final_hd'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<FinalHD %r>' % self.id


class FinalZK(BaseFinal):
    __tablename__ = 'final_zk'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<FinalZK %r>' % self.id


class FinalLM(BaseFinal):
    __tablename__ = 'final_lm'
    __bind_key__ = 'kakou'

    def __repr__(self):
        return '<FinalLM %r>' % self.id


class FinalBL(BaseFinal):
    __tablename__ = 'final_bl'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<FinalBL %r>' % self.id


class BaseLog(db.Model):
    """基础表"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    final_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)

    def __init__(self, final_id=1, date_created=None):
        self.final_id = final_id
        self.date_created = date_created

    def __repr__(self):
        return '<BaseLog %r>' % self.id


class LogHCQ(BaseLog):
    __tablename__ = 'log_hcq'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<LogHCQ %r>' % self.id


class LogDYW(BaseLog):
    __tablename__ = 'log_dyw'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<LogDYW %r>' % self.id


class LogHY(BaseLog):
    __tablename__ = 'log_hy'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<LogHY %r>' % self.id


class LogHD(BaseLog):
    __tablename__ = 'log_hd'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<LogHD %r>' % self.id


class LogZK(BaseLog):
    __tablename__ = 'log_zk'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<LogZK %r>' % self.id


class LogLM(BaseLog):
    __tablename__ = 'log_lm'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<LogLM %r>' % self.id


class LogBL(BaseLog):
    __tablename__ = 'log_bl'
    __bind_key__ = 'kakou'
    
    def __repr__(self):
        return '<LogBL %r>' % self.id