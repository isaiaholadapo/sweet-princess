from django.db import models

# Create your models here.


class Contact(models.Model):
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.fullname
