#!coding=UTF-8

import time
from flask import url_for, jsonify, abort, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from init import *
from models import User, Betting, Lottery
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
    column_list = ('id', 'username' , 'password', 'invite')
    column_labels = {'id':u'序号',
        'username' : u'用户名',
        'password' : u'密 码',
        'payment':u'支付宝/微信',
        'invite':u'邀请码'
        }

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
            vals = User(username=user, payment=style, password=pwd,  invite=invite)
            print vals

            if vals is None:
                info = jsonify({'code':False,'error': 'not create'})
            db.session.add(vals)
            db.session.commit()
        except Exception, e:
            import sys
            return  jsonify({'code':False,'error': 400})
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
    column_list = ('id', 'user' , 'chip' , 'Raise', )

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

            man = User.query.filter_by(username=user).first()
            vals = Betting(chip=chip,Raise=ray,user_id=man.id)
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


class MyLotteryView(ModelView):
    column_labels = {
    'id':u'序号',
    'number':u'设置开奖号码',
    'times':u'开奖间隔',
    'dates':u'固定开奖时间',
    }
    # can_create = False
    column_list = ('id', 'number' , 'times','dates')


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

# admin.init_app(app)

if __name__ == '__main__':

    # Start app
    print(app.url_map)
    manager.run()
    app.run()