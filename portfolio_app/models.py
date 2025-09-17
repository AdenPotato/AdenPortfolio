from django.db import models
from django.urls import reverse

# Create your models here.

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    about = models.CharField(blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio-detail', args=[str(self.id)])
    
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField()

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])
    

class Student(models.Model):
#List of choices for major value in database, human readable name
    MAJOR = (
        ('CSCI-BS', 'BS in Computer Science'),
        ('CPEN-BS', 'BS in Computer Engineering'),
        ('BIGD-BI', 'BI in Game Design and Development'),
        ('BICS-BI', 'BI in Computer Science'),
        ('BISC-BI', 'BI in Computer Security'),
        ('CSCI-BA', 'BA in Computer Science'),
        ('DASE-BS', 'BS in Data Analytics and Systems Engineering')
    )
    name = models.CharField(max_length=200)
    email = models.CharField("MSU Email", max_length=200)
    major = models.CharField(max_length=200, choices=MAJOR)
    portfolio = models.OneToOneField(
        Portfolio,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='student', 
    )
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])
    