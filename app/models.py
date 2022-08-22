# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Student(models.Model):
    stu_id = models.IntegerField(primary_key=True)
    stu_name = models.CharField(max_length=10, blank=True, null=True)
    stu_gender = models.CharField(max_length=1, blank=True, null=True)
    pic = models.TextField(blank=True, null=True)
    id = models.CharField(max_length=18, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    province = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=30, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    college = models.CharField(max_length=20, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    major = models.CharField(max_length=20, blank=True, null=True)
    class_number = models.IntegerField(blank=True, null=True)
    politics_statue = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    risk = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Teacher(models.Model):
    tea_id = models.IntegerField(primary_key=True)
    college = models.CharField(max_length=20, blank=True, null=True)
    tea_gender = models.CharField(max_length=1, blank=True, null=True)
    tea_name = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher'


class Mail(models.Model):
    stu_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail'


class Covid(models.Model):
    area = models.CharField(max_length=100, blank=True, null=True)
    risk = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covid'


class High(models.Model):
    province = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=30, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'high'


class Middle(models.Model):
    province = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=30, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'middle'


class Low(models.Model):
    province = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=30, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'low'


class Newcovid(models.Model):
    time = models.CharField(primary_key=True, max_length=30)
    confirm = models.IntegerField(blank=True, null=True)
    confirm_add = models.IntegerField(blank=True, null=True)
    wzz = models.IntegerField(blank=True, null=True)
    wzz_add = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'newcovid'
