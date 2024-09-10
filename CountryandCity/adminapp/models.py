from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver


# # Create your models here.


class Timebasedmodel(models.Model):
	created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	modified_on = models.DateTimeField(auto_now=True,null=True,blank=True) 

	class Meta:
		abstract=True


class User(AbstractUser,Timebasedmodel):
	user_type = models.CharField(max_length=200,null=True,blank=True)
	dob = models.DateField(max_length=80,null=True,blank=True)
	email = models.TextField(null=True,blank=True)
	phone_no  = models.TextField(null=True,blank=True)
	username = models.TextField(null=True,blank=True,unique=True)
	created_by = models.CharField(max_length=50,null=True,blank=True)
	modified_by = models.CharField(max_length=50,null=True,blank=True)
	focus_area = models.TextField(null=True, blank=True)
	treatment_approach = models.TextField(null=True, blank=True)
	is_approve = models.BooleanField(default=False)
	is_recomended = models.BooleanField(default=False)
	doctor_name = models.TextField(null=True, blank=True)
	consultation_link = models.TextField(null=True, blank=True)
	uid = models.TextField(null=True,blank=True)
	user_segment=models.BooleanField(default=False)
	password = models.CharField(max_length=100,blank=True,null=True)
	email_verify = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def role_creation(sender, instance, created, **kwargs):
	if created:
		if (instance.user_type==None) or (instance.user_type==''):
			instance.user_type='Admin'
			instance.save(update_fields=['user_type',])


from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
