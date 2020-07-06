from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""  Creates and saves a User with the given username, email and password.
		"""
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff',False)
		extra_fields.setdefault('is_superuser',False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff',True)
		extra_fields.setdefault('is_superuser',True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff =True')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser = True')
			return self._create_user(email,password,**extra_fields)

class PortalUser(AbstractUser):
	USER_TYPES =(
		('patient','patient'),
		('doctor','doctor'),
		('examiner','examiner')
		)
	first_name = models.CharField(max_length=20,null=True,blank=True)
	last_name = models.CharField(max_length=20,null=True,blank=True)
	username = models.CharField(max_length=20,null=True,blank=True)
	email = models.EmailField(unique=True,null=False,blank=False)
	address = models.CharField(max_length=100)
	phone = models.CharField(max_length=50)
	user_type = models.CharField(max_length=32,choices=USER_TYPES)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_by = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
	updated_date = models.DateTimeField(auto_now_add=True)
	is_verified = models.BooleanField(default=False,verbose_name='Verfied')
	image = models.ImageField(null=True,blank=True,upload_to='media/images/user/%Y-%m-%d/')
	objects = UserManager()
	USERNAME_FIELD='email'
	REQUIRED_FIELDS=[]

	def get_full_name(self):
		return '{} {}'.format(self.first_name, self.last_name)

	def __str__(self):
		return self.email

class Patient(models.Model):
	user=models.ForeignKey(PortalUser,on_delete=models.CASCADE,related_name='patient')
	is_active=models.BooleanField(default=False)

	def __str__(self):
		return self.user.email

class DoctorSpeciality(models.Model):
	name=models.CharField(max_length=50)
	is_active=models.BooleanField(default=False)

	def __str__(self):
		return self.name
from hospital.models import Hospital

class Doctor(models.Model):
	user=models.ForeignKey(PortalUser,on_delete=models.CASCADE,related_name='doctor')
	license_id=models.CharField(max_length=40)
	is_active=models.BooleanField(default=False)
	speciality=models.ManyToManyField(DoctorSpeciality,related_name='speciality')
	degree=models.CharField(max_length=50)
	hospital=models.ManyToManyField(Hospital,related_name='hospital')

	def __str__(self):
		return self.user.email

class Examiner(models.Model):
	user=models.ForeignKey(PortalUser,on_delete=models.CASCADE,related_name='examiner')
	license_id=models.CharField(max_length=40)
	is_active=models.BooleanField(default=False)
	degree=models.CharField(max_length=50)
	hospital=models.ManyToManyField(Hospital,related_name='examiner_hospital')
	lab_details=models.TextField()

	def __str__(self):
		return self.user.email

# class UserPasswordReset(models.Model):
#     user = models.ForeignKey(PortalUser, on_delete=models.CASCADE, related_name='requesting_user')
#     key = models.CharField(max_length=16)
#     created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.user.email


# comma_separated_float_list_re = re.compile('^([-+]?\d*\.?\d+[,\s]*)+$')
# validate_comma_separated_float_list = RegexValidator(
#               comma_separated_float_list_re, 
#               _(u'Enter only floats separated by commas.'), 'invalid')

# class CommaSeparatedFloatField(CharField):
#     default_validators = [validators.validate_comma_separated_float_list]
#     description = _("Comma-separated floats")

#     def formfield(self, **kwargs):
#         defaults = {
#             'error_messages': {
#                 'invalid': _(u'Enter only floats separated by commas.'),
#             }
#         }
#         defaults.update(kwargs)
#         return super(CommaSeparatedFloatField, self).formfield(**defaults)

		

		





