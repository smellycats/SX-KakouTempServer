# -*- coding: utf-8 -*-
import arrow

from . import db


class Users(db.Model):
    """用户"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    password = db.Column(db.String(128))
    scope = db.Column(db.String(128), default='')
    date_created = db.Column(db.DateTime, default=arrow.now().datetime)
    date_modified = db.Column(db.DateTime, default=arrow.now().datetime)
    banned = db.Column(db.Integer, default=0)

    def __init__(self, username, password, scope='', banned=0,
                 date_created=None, date_modified=None):
        self.username = username
        self.password = password
        self.scope = scope
        now = arrow.now().datetime
        if not date_created:
            self.date_created = now
        if not date_modified:
            self.date_modified = now
        self.banned = banned

    def __repr__(self):
        return '<Users %r>' % self.id


class Scope(db.Model):
    """权限范围"""
    __tablename__ = 'scope'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Scope %r>' % self.id


class TempDYW(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_dyw'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempDYW %r>' % self.id


class TempHCQ1(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_hcq1'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempHCQ1 %r>' % self.id


class TempHCQ2(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_hcq2'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempHCQ2 %r>' % self.id

class TempHCQ3(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_hcq3'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempHCQ3 %r>' % self.id

class TempHY(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_hy'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempHY %r>' % self.id


class TempHD(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_hd'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempHD %r>' % self.id


class TempZK(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_zk'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempZK %r>' % self.id


class TempLM(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'temp_lm'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, flag, banned):
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
        return '<TempLM %r>' % self.id


class FinalHCQ(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'final_hcq'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, imgpath, flag):
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

    def __repr__(self):
        return '<FinalHCQ %r>' % self.id


class FinalZK(db.Model):
    """仲恺最终表"""
    __tablename__ = 'final_zk'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, imgpath, flag):
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

    def __repr__(self):
        return '<FinalZK %r>' % self.id


class FinalDYW(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'final_dyw'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, imgpath, flag):
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

    def __repr__(self):
        return '<FinalDYW %r>' % self.id


class FinalHY(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'final_hy'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, imgpath, flag):
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

    def __repr__(self):
        return '<FinalHY %r>' % self.id


class FinalHD(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'final_hd'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, imgpath, flag):
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

    def __repr__(self):
        return '<FinalHD %r>' % self.id


class FinalLM(db.Model):
    """大亚湾临时表1"""
    __tablename__ = 'final_lm'
    __bind_key__ = 'kakou'
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

    def __init__(self, cltx_id, hphm, jgsj, hpys, hpys_id, hpys_code, kkdd,
		 kkdd_id, fxbh, fxbh_code, cdbh, clsd, hpzl, kkbh, clbj,
		 imgurl, imgpath, flag):
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

    def __repr__(self):
        return '<FinalLM %r>' % self.id