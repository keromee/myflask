#!coding=UTF-8
from  init import *

class User(db.Model):
    '''
    username 	帐号
    payment	支付宝 / 微信
    password 	密码
    addition 	附加码
    invite 		邀请码
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    payment = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)
    addition = db.Column(db.String(80))
    invite = db.Column(db.String(80))
    # model1 = db.relationship('Betting', foreign_keys='UserNote.user_id',backref='user', lazy="dynamic") 

    def __repr__(self):
        return self.username


class Betting(db.Model):
    '''
    id
    user_id 外键User表
    chip 需要下注的数字筹码，list
    Raise 注码
    '''
    __tablename__ = 'bettinglist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chip = db.Column(db.String(80), nullable=False)
    Raise = db.Column(db.Integer, nullable=False)
    user = db.relationship(User,
                           foreign_keys='Betting.user_id',
                           backref=db.backref('user', order_by=id))

    # def __init__(self, **kwargs):
    #     super(Betting, self).__init__(**kwargs)
        # inline_models = [('bettinglist', dict(form_columns=['user_id']))]

    def __repr__(self):
        return self.user_id.username


class Lottery(db.Model):
    '''
    Number    奖号
    times       开奖间隔时间  PS=分钟为单位
    dates       固定开奖时间  PS=当有固定开奖时间时，忽略times
    '''
    __tablename__ = 'lottery'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    times = db.Column(db.String(80), nullable=False)
    dates = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Number %r>' % self.number

# db.event.listen(Lottery.number, 'set', Lottery.on_changed_body)