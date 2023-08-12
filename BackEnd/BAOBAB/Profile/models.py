from django.db import models

class Profile(moedls.Model):
    user_id = models.OneToOneField('User.User', on_delete=models.CASCADE)
    