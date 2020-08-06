from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, SelectField, SelectMultipleField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class newOpportunity(FlaskForm):
    customerName = StringField('Customer Name', validators=[DataRequired()])
    desc         = StringField('Description', validators=[Length(min=0, max=500)])
    submit       = SubmitField('Submit')

class opportunitySave(FlaskForm):
    customerName = StringField('Customer Name', validators=[DataRequired()])
    desc         = StringField('Description', validators=[Length(min=0, max=500)])
    contractTerm = IntegerField('Contract Term', validators=[DataRequired()])
    submit       = SubmitField('Save')

class loginForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Submit')

class addUserForm(FlaskForm):
    firstName        = StringField('First Name', validators=[DataRequired()])
    lastName         = StringField('Last Name', validators=[DataRequired()])
    email            = StringField('Email', validators=[DataRequired(), Email()])
    jobTitle         = StringField('Job Title', validators=[DataRequired()], default='Sales')
    password         = PasswordField('Password', validators=[DataRequired()])
    confirmPassword  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    isActive         = BooleanField('Is Active?', default=True)
    #manager         = StringField(
    accessLevel      = IntegerField('Access Level', default=1)
    businessLine     = StringField('Business Line', default='Cloud Services')
    submit           = SubmitField('Submit')

class changePassForm(FlaskForm):
    currentPassword  = PasswordField('Current Password', validators=[DataRequired()])
    password         = PasswordField('New Password', validators=[DataRequired()])
    confirmPassword  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit           = SubmitField('Submit')

class getConfirmationForm(FlaskForm):
    submit = SubmitField('Confirm')

# DEPRECATED:
#    Deprecated in favor of just referencing the 'name' of individual elements in the HTML to get line-by-line updates.
#######################################################################################################################
# class lineItemForm(FlaskForm):
#     selected = BooleanField('Selected')
#     qtyNew   = IntegerField('Qty New', validators=[DataRequired()])
#     qtyExi   = IntegerField('Qty Exi', validators=[DataRequired()])
#     discNRC  = DecimalField('Disc % NRC', validators=[DataRequired()], places=2, rounding=None, number_format=None, use_locale=False)
#     discMRC  = DecimalField('Disc % MRC', validators=[DataRequired()], places=2, rounding=None, number_format=None, use_locale=False)
