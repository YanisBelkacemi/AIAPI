#NEEDS A FUCKING REVIEW 


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiKeys(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    key_prefix = models.CharField(max_length=10)
    key_hash = models.TextField()
    name = models.CharField(max_length=50, blank=True, null=True)
    revoked = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    last_used = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_keys'


class Models(models.Model):
    name = models.CharField(unique=True, max_length=50)
    provider = models.CharField(max_length=50)
    version_model = models.CharField(max_length=50, blank=True, null=True)
    max_tokens = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'models'


class RateLimits(models.Model):
    api_key = models.ForeignKey(ApiKeys, models.DO_NOTHING)
    requests_per_minute = models.IntegerField(blank=True, null=True)
    requests_per_day = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rate_limits'


class Requests(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    api_key = models.ForeignKey(ApiKeys, models.DO_NOTHING)
    model = models.ForeignKey(Models, models.DO_NOTHING)
    prompt = models.TextField()
    response = models.TextField(blank=True, null=True)
    tokens_used = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requests'


class UsageStats(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    date = models.DateField()
    requests_count = models.IntegerField(blank=True, null=True)
    tokens_used = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usage_stats'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.TextField()
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    userinputid = models.CharField(db_column='UserInputID', unique=True, max_length=10)  # Field name made lowercase.
    useroutputid = models.CharField(db_column='UserOutputID', unique=True, max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
