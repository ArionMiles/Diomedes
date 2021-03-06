from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Dimensions:
    CHOICES = (
        ('2D', '2D'),
        ('2D 4DX', '2D 4DX'),
        ('3D', '3D'),
        ('3D 4DX', '3D 4DX'),
        ('IMAX 2D', 'IMAX 2D'),
        ('IMAX 3D', 'IMAX 3D'),
    )

class Languages:
    CHOICES = (
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Tamil', 'Tamil'),
        ('Punjabi', 'Punjabi'),
        ('Telugu', 'Telugu'),
        ('Kannada', 'Kannada'),
        ('Malayalam', 'Malayalam')
    )

class Region(models.Model):
    code = models.CharField(max_length=20, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    alias = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class SubRegion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, null=True, blank=True, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    subregion = models.ForeignKey(SubRegion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Reminder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    theaters = models.ManyToManyField(Theater, related_name="reminders", through="TheaterLink")
    name = models.CharField(max_length=200)
    language = models.CharField(max_length=20, default="Hindi", choices=Languages.CHOICES)
    dimension = models.CharField(max_length=20, default="2D", choices=Dimensions.CHOICES)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    dropped = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({}) - {} - {} ".format(self.name, self.language, self.dimension, self.date)

class TheaterLink(models.Model):
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    found = models.BooleanField(default=False)
    found_at = models.DateTimeField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    subregion = models.ForeignKey(SubRegion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile')

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
