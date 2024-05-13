from django.db import models
from django.utils import timezone
from django.db.models import JSONField


# In[temp]
class TempData(models.Model):
    i = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    value = models.FloatField(null=False)
    date = models.DateTimeField(null=False, default=timezone.now)


# In[raw json]
class JsonShort(models.Model):
    i = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    TX = JSONField()
    RX = JSONField()
    Operation = JSONField()
    AllPCs = JSONField()
    SNMPAgents = JSONField()
    SherkatNet = JSONField()
    RXNet = JSONField()
    TxNet = JSONField()
    date = models.DateTimeField(null=False, default=timezone.now)


class JsonLong(models.Model):
    i = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)
    AllData = JSONField()
    Date = models.DateTimeField(null=False, default=timezone.now)


# In[Organized]
class Net(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    Values = JSONField(null=True)
    Date = models.DateTimeField(null=False, default=timezone.now)


class Snmp(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    Values = JSONField(null=True)
    Date = models.DateTimeField(null=False, default=timezone.now)


class Tx(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    Values = JSONField(null=True)
    Message = models.CharField(max_length=200, null=True, blank=True)
    Date = models.DateTimeField(null=False, default=timezone.now)


class Ctc(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    Values = JSONField(null=True)
    Message = models.CharField(max_length=200, null=True, blank=True)
    TimeLabel = models.CharField(max_length=50, null=True)
    TimeLabelIntegrated = models.CharField(max_length=50, null=True)
    NRXIntegrated = models.CharField(max_length=50, null=True)
    RXValues = JSONField(null=True)
    Date = models.DateTimeField(null=False, default=timezone.now)


class SigPrc(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    Values = JSONField(null=True)
    ChProps = JSONField(null=True)
    TimeLabel = models.CharField(max_length=50, null=True)
    Date = models.DateTimeField(null=False, default=timezone.now)


class Pcs(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    Values = JSONField(null=True)
    MemPer = models.CharField(max_length=50, null=True)
    CPULoad = models.CharField(max_length=50, null=True)
    HDDValues = JSONField(null=True)
    Cores = JSONField(null=True)
    Date = models.DateTimeField(null=False, default=timezone.now)


class Adsb(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    Message = models.CharField(max_length=200, null=True, blank=True)
    UpTime = models.CharField(max_length=50, null=True)
    FrameRate = models.CharField(max_length=50, null=True)
    Connected = models.CharField(max_length=50, null=True)
    Date = models.DateTimeField(null=False, default=timezone.now)


class Operation(models.Model):
    i = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=50, null=False)
    Name = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True)
    IP = models.CharField(max_length=50, null=True)
    NLayer = models.CharField(max_length=50, null=True)
    AX = models.CharField(max_length=50, null=True)
    AY = models.CharField(max_length=50, null=True)
    UpTime = models.CharField(max_length=50, null=True, blank=True)
    Layers = JSONField(null=True)
    Date = models.DateTimeField(null=False, default=timezone.now)
