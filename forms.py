#!coding=UTF-8
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms.validators import Required

# 这是打个标记
class ChipForm(FlaskForm):
	user_id = IntegerField('openid', validators = [Required()])
	chip = StringField("下注..", validators=[Required()])
	Raise = IntegerField('注码..', default = False)
