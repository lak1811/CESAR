from django.db import models

# Create your models here.


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CapitulosDeLivrosPublicados(models.Model):
    Nome = models.CharField(max_length=100,default="")
    Title = models.CharField(max_length=500)
    Year = models.CharField(max_length=100, default='')
    Lang = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)

class Education(models.Model):
    Nome = models.CharField(max_length=100)
    Year_INI = models.CharField(max_length=10)
    Year_FIN = models.CharField(max_length=10, null=True, blank=True)
    Month_INI = models.CharField(max_length=20)
    Month_FIN = models.CharField(max_length=20, null=True, blank=True)
    Course = models.CharField(max_length=200, default='')
    Type = models.CharField(max_length=100, null=True, blank=True)
    Discipline = models.CharField(max_length=100, null=True, blank=True)

class OtherProductions(models.Model):
    Fullname = models.CharField(max_length=100)
    YEAR = models.CharField(max_length=30)
    NATURE = models.CharField(max_length=50, null=True, blank=True)
    INSTITUTION = models.CharField(max_length=100, null=True, blank=True)
    COURSE = models.CharField(max_length=100, default='')
    STUDENT = models.CharField(max_length=100, null=True, blank=True)
    TYPE = models.CharField(max_length=50, null=True, blank=True)
    SPONSOR = models.CharField(max_length=100, null=True, blank=True)

class Person(models.Model):
    ID = models.CharField(max_length=200,primary_key=True)
    Full_name = models.CharField(max_length=100, null=True, blank=True)
    Last_Name = models.CharField(max_length=50)
    Citation=models.CharField(max_length=100,default='')
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Description = models.TextField()
    Workplace = models.CharField(max_length=50)
    Update = models.CharField(max_length=50,default='')
    ORCID = models.CharField(max_length=100)
    
    

class ProducaoTecnica(models.Model):
    Fullname = models.CharField(max_length=100, default='')
    Course = models.CharField(max_length=200, default='')
    Year = models.IntegerField(default=0)
    Integrantes = models.CharField(max_length=300, null=True, blank=True)

class Project(models.Model):
    Fullname = models.CharField(max_length=100)
    Proj = models.CharField(max_length=500)
    YEAR_INI = models.CharField(max_length=30)
    YEAR_FIN = models.CharField(max_length=30)
    Natureza = models.CharField(max_length=500, null=True, blank=True)
    Integrantes = models.CharField(max_length=500, null=True, blank=True)
    Cordena = models.CharField(max_length=500, null=True, blank=True)

class Publications(models.Model):
    Fullname = models.CharField(max_length=100, default='')
    TITLE = models.CharField(max_length=600, null=True, blank=True)
    YEAR = models.IntegerField(null=True, blank=True)
    DOI = models.CharField(max_length=100, null=True, blank=True)
    LANG = models.CharField(max_length=500, null=True, blank=True)
    JOURNAL = models.CharField(max_length=300, null=True, blank=True)
    ISSN = models.CharField(max_length=100, default='')
    AUTHOR = models.CharField(max_length=200, null=True, blank=True)

class Trabalho(models.Model):
    fullname = models.CharField(max_length=255)  # Full name attribute
    TITLE = models.CharField(max_length=255)
    YEAR = models.CharField(max_length=30)
    DOI = models.CharField(max_length=100)
    LANG = models.CharField(max_length=50)
    AUTHOR = models.CharField(max_length=255)
    ORDER = models.CharField(max_length=50) 
    ORDER_OK = models.CharField(max_length=50)  