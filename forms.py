from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, MultipleFileField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email

class ServiceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    images = MultipleFileField('Images')
    submit = SubmitField('Submit')

class AnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    images = MultipleFileField('Images')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    role = SelectField('Rôle', choices=[('employee', 'Employé'), ('veterinarian', 'Vétérinaire')], validators=[DataRequired()])
    submit = SubmitField('Créer un compte')