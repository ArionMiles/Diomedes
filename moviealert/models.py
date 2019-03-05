from django.db import models

# Create your models here.

class Dimensions:
    CHOICES = (
        ('2D', '2D'),
        ('2D 4DX', '2D 4DX'),
        ('3D', '3D'),
        ('3D 4DX', '3D4X'),
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

class Task(models.Model):
    username = models.EmailField()
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
