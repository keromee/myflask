#!coding=UTF-8

import time
from flask import url_for, jsonify, abort, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from init import *
from models import User, Betting, Lottery, Recode
from flask_admin import Admin, BaseView, expose,AdminIndexView
from json import loads,dumps
from forms import ChipForm

# Create custom admin view
class MyAdminView(BaseView):
    @expose('/')
    def index(self):
        # form = LoginForm()
        # name = time.strftime("%b %d, %Y - %H:%M:%S")
        # digits = [1,2,3,4,u'你好',5]
        # colname = [u'开奖号码', u'开奖间隔', u'固定开奖时间']
        return self.render('admin.html')

    @expose('/saveof', methods=('GET', 'POST'))
    def saveof(self):
        # num = request.form['number']
        # reg = request.form['regular']
        # space = request.form['spacing']
        print "num, reg, space"
        return render_template('admin.html')


class MyUserView(ModelView):
    can_create = False
    column_list = ('id', 'username' , 'password', 'invite', 'point')
    column_labels = {'id':u'序号',
        'username' : u'用户名',
        'password' : u'密 码',
        'payment':u'支付宝/微信',
        'invite':u'邀请码',
        'point':u'积 分',
        }

    @expose('/api/v1.0/login', methods=['POST'])
    def query_task(self):
        print '+++++++++++',request
        if not request.json:
            abort(400)
        info = {}
        
        try:
            user = request.json.get('username','')
            pwd = request.json.get('password','')
            if not user and pwd:
                raise ValueError, u'不可用的参数'

            vals = User.query.filter_by(username=user,password=pwd).first()
            if vals is None:
                info = jsonify({'code':False,'error': 'Not found'})
            else:
                info = jsonify({'code':True,'msg': 'OK', 'value':vals.point})
        except Exception, e:
            return  jsonify({'code':False,'error': 400})
        return info

    @expose('/api/v1.0/newUser', methods=['POST'])
    def create_task(self):
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        print '==!!==',request.json
        try:
            user = request.json.get('username','')
            pwd = request.json.get('password','')
            style = request.json.get('payment','')
            invite = request.json.get('invite','')
            # if not user and not pwd :
            #     raise ValueError, u'不可用的参数'

            print "===dadad", type(user.encode('utf-8')), type("哟哟")
            vals = User(username=user.encode('utf-8'), payment=style, password=pwd,  invite=invite)
            print "===ffff",vals

            if vals is None:
                info = jsonify({'code':False,'error': 'not create'})

            db.session.add(vals)
            db.session.commit()
            db.session.rollback()
        except Exception, e:
            db.session.rollback()
            info = jsonify({'code':False,'error': 400})
            return info
        return info

class MyBettingView(ModelView):
    # inline_models = [('bettinglist', dict(form_columns=['user_id']))]
    # inline_models = (MyUserView(User),)
    column_labels = {
    'id':u'序号',
    'chip':u'筹 码',
    'Raise':u'注 码',
    'user':u'关联'
    }
    can_create = False
    column_list = ('id', 'user' , 'chip' , 'Raise', 'check')

    # @expose('/', methods=['GET', 'POST'])
    # def index(self):
    #     form = ChipForm()
    #     return self.render('myadmin.html', form=form)
    
    @expose('/api/v1.0/Betting', methods=['POST'])
    def Betting_task(self):
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        print '!!!!',request.json
        try:
            user = request.json.get('username','')
            chip = request.json.get('chip','')
            ray = request.json.get('Raise',0)
            point = request.json.get('point',0)

            man = User.query.filter_by(username=user).first()
            man.point = point
            vals = Betting(chip=chip,Raise=ray,user_id=man.id)
            db.session.add(vals)
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            info = jsonify({'code':False,'error': 400})
            return info
        return info

    @expose('/api/v1.0/Betting_query', methods=['POST'])
    def Betting_query(self):
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        try:
            user = request.json.get('username','')
            man = User.query.filter_by(username=user).first()
            vals = Betting.query.filter_by(user_id=man.id).first()
            if vals is None:
                info = jsonify({'code':False,'error': 'Not found'})
            else:
                info = jsonify({'code':True,'msg': 'OK', 'point':man.point, 'value':vals.Raise})
            # vals.check = True
            # db.session.add(vals)
            # db.session.commit()
        except Exception, e:
            # db.session.rollback()
            info = jsonify({'code':False,'error': 400})
            return info
        return info

    # @expose('/api/v1.0/histroy', methods=['POST'])
    # def show_histroy(self):
    #     if not request.json:
    #         abort(400)
    #     info = jsonify({'code':True,'msg': 'OK'})
    #     try:
    #         user = request.json.get('username','')
    #         v1 = User.query.filter_by(username=user).first()

            
    #         v2 = Betting.query.filter_by(user_id=v1.id).first()
    #         info = jsonify({'code':True,'msg': 'OK','value':v2.chip})
    #     except Exception, e:
    #         return  jsonify({'code':False,'error': 400})
    #     return info 


class MyLotteryView(ModelView):
    column_labels = {
    'id':u'序号',
    'number':u'设置开奖号码',
    'times':u'开奖间隔',
    'dates':u'固定开奖时间',
    }
    # can_create = False
    column_list = ('id', 'number' , 'times','dates')

    @expose('/api/v1.0/Lottery', methods=['GET'])
    def set_time(self):
        info = jsonify({'code':True,'msg': 'OK'})
        try:
            res = db.session.query(Lottery.number,Lottery.times,db.func.max(Lottery.dates).label('ml')).first()
            print res
            info = jsonify({'code':True,'msg': 'OK','value':res})
        except Exception, e:
            db.session.rollback()
            info = jsonify({'code':False,'error': 400})
            return info
        return info

    @expose('/api/v1.0/histroy', methods=['GET'])
    def show_histroy(self):
        info = jsonify({'code':True,'msg': 'OK'})
        try:
            # v = Lottery.query.all()
            # db.session.query(Lottery.number).all()
            v = Lottery.query.with_entities(Lottery.number).all()
            info = jsonify({'code':True,'msg': 'OK','value':['%d' % i[0] for i in v]})
            print '==-=-=-=',info
        except Exception, e:
            return  jsonify({'code':False,'error': 400})
        return info 


class MyRecodeview(ModelView):
    column_labels = {
    'id':u'序号',
    'state':u'上/下分',
    'cost':u'金 额',
    'user2':u'关 联'
    }

    column_list = ('id', 'user2' , 'cost','state')

    @expose('/api/v1.0/Recode', methods=['POST'])
    def create_task(self):
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        print '!!!!',request.json
        try:
            user = request.json.get('username','')
            cost = request.json.get('cost',0.0)
            state = request.json.get('state',False)

            man = User.query.filter_by(username=user).first()
            if state:
                man.point += int(cost)
            else:
                _sub= man.point - int(cost) 
                if _sub <0:
                    info = jsonify({'code':False,'error': "只能下：%d分" % man.point})
                    return info
                man.point = _sub
            vals = Recode(cost=cost,state=state,user_id=man.id)
            db.session.add(vals)
            db.session.add(man)
            db.session.commit()
            info = jsonify({'code':True,'msg': 'OK','score':man.point})
        except Exception, e:
            db.session.rollback()
            info = jsonify({'code':False,'error': 400})
            return info
        return info

class AnotherAdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('anotheradmin.html')

    @expose('/test/')
    def test(self):
        return self.render('test.html')

    @expose('/api/v1.0/login', methods=['POST'])
    def query_task(self):
        print '+++++++++++',request
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        
        try:
            user = request.json.get('username','')
            pwd = request.json.get('password','')
            if not user and pwd:
                raise ValueError, u'不可用的参数'

            vals = User.query.filter_by(username=user,password=pwd).first()
            print "------------=====", req
            if vals is None:
                info = jsonify({'code':False,'error': 'Not found'})
        except Exception, e:
            return  jsonify({'code':False,'error': 400})
        return info

    @expose('/api/v1.0/newUser', methods=['POST'])
    def create_task(self):
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        print '==!!==',request.json
        try:
            user = request.json.get('username','')
            pwd = request.json.get('password','')
            style = request.json.get('payment','')
            invite = request.json.get('invite','')
            # if not user and not pwd :
            #     raise ValueError, u'不可用的参数'

            print "===dadad"
            vals = User(user, style, pwd,  invite)
            print vals

            if vals is None:
                info = jsonify({'code':False,'error': 'not create'})
            db.session.add(vals)
            db.session.commit()
        except Exception, e:
            import sys
            return  jsonify({'code':False,'error': 400})
        return info

    @expose('/api/v1.0/Betting', methods=['POST'])
    def Betting_task(self):
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        print '!!!!',request.json
        try:
            user = request.json.get('username','')
            chip = request.json.get('chip','')
            ray = request.json.get('Raise',0)

            vals = Betting()
            db.session.add(vals)
            db.session.commit()
        except Exception, e:
            return  jsonify({'code':False,'error': 400})
        return info

    @expose('/api/v1.0/histroy', methods=['POST'])
    def show_histroy(self):
        if not request.json:
            abort(400)
        info = jsonify({'code':True,'msg': 'OK'})
        try:
            user = request.json.get('username','')
            v1 = User.query.filter_by(username= user).first()

            v2 = Betting.query.filter_by(user_id=v1.id).first()
            print v2, v1.id
            info = jsonify({'code':True,'msg': 'OK','value':v2.chip})
        except Exception, e:
            return  jsonify({'code':False,'error': 400})
        return info

# Create admin interface
admin = Admin(
    app,
    index_view=AdminIndexView(
        name=u'导航栏',
        template='test.html',
        url='/admin'
    )
)
# admin.locale_selector(get_locale)
# admin.add_view(MyAdminView(name=u"开奖设置"))
# admin.add_view(AnotherAdminView(name="view2", ))
admin.add_view(MyUserView(User, db.session, name=u'用户'))
admin.add_view(MyBettingView(Betting, db.session, name=u'注码记录'))
admin.add_view(MyLotteryView(Lottery, db.session, name=u'开奖设置'))
admin.add_view(MyRecodeview(Recode, db.session, name=u'充值记录'))

# admin.init_app(app)

if __name__ == '__main__':

    # Start app
    print(app.url_map)
    manager.run()
    app.run()