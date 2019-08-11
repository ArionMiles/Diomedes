from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.

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
    subregion_code = models.CharField(max_length=20, null=True, blank=True)
    subregion_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.subregion_name

class Task(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    city = models.ForeignKey(Region, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=200)
    movie_language = models.CharField(max_length=20, default='Hindi', choices=Languages.CHOICES)
    movie_dimension = models.CharField(max_length=20, default="2D", choices=Dimensions.CHOICES)
    movie_date = models.DateField()
    task_completed = models.BooleanField(default=False)
    search_count = models.IntegerField(default=0)
    dropped = models.BooleanField(default=False)

    def __str__(self):
        return "<{} ({}) ({}) | {} >".format(self.movie_name, self.movie_language, self.movie_dimension, self.movie_date)

class Theater(models.Model):
    name = models.CharField(max_length=200)
    venue_code = models.CharField(max_length=20, null=True, blank=True)
    subregion = models.ForeignKey(SubRegion, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Reminder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    venues = ArrayField(models.CharField(max_length=5), blank=True, null=True)
    name = models.CharField(max_length=200)
    language = models.CharField(max_length=20, default='Hindi', choices=Languages.CHOICES)
    dimension = models.CharField(max_length=20, default="2D", choices=Dimensions.CHOICES)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    dropped = models.BooleanField(default=False)
    found_time = JSONField(default=list)

    def __str__(self):
        return "<{} ({}) ({}) | {} >".format(self.name, self.language, self.dimension, self.date)

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


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
