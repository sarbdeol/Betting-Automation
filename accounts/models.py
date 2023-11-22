from django.db import models


class UserAccountManager(models.Manager):
    def active_accounts(self):
        return self.filter(is_active=True)


class UserAccount(models.Model):
    WEBSITE_CHOICES = [
        ('Sportybet', 'Sportybet'),
        ('Xbet', 'Xbet'),
        ('Betway', 'Betway'),
    ]
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    website = models.CharField(max_length=20, choices=WEBSITE_CHOICES)

    def __str__(self):
        return self.username

    objects = UserAccountManager()


class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
