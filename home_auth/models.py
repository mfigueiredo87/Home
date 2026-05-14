from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    # Adicione campos personalizados aqui, se necessário
   username = models.CharField(max_length=254, unique=True)
   email = models.EmailField(max_length=254, unique=True)
   first_name = models.CharField(max_length=254, blank=True)
   last_name = models.CharField(max_length=254, blank=True)
   date_joined= models.DateTimeField(auto_now_add=True)
   is_authorized = models.BooleanField(default=True)
   
#definindo os tres niveis de autenticacao
   is_student = models.BooleanField(default=False)
   is_teacher = models.BooleanField(default=False)
   is_admin = models.BooleanField(default=False)
   
#    definindo grups
   groups = models.ManyToManyField(
         'auth.Group',
         related_name = 'customuser_groups',
         blank = True
    )
# definindo permissoes
   user_permissions = models.ManyToManyField(
            'auth.Permission',
            related_name = 'customuser_permissions',
            blank = True
    )

   def __str__(self):
        return self.username

# defindo class para reset da password
class PasswordResetRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

# definindo a validade do token para reset da password
    TOKEN_VALIDITY_PERIOD = timezone.timedelta(hours=1)
    
    def is_valid(self):
        return timezone.now() < self.created_at + self.TOKEN_VALIDITY_PERIOD
    
    def send_reset_email(self):
        reset_link = f"http://localhost:8000/reset-password/{self.token}/"
        send_mail(
            'Password Reset Request',
            f'Clica no link para redefinir sua senha: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )
        
    def __str__(self):
        return f"Password reset request for {self.user.username} at {self.created_at}"