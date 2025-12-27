from django.db import models
from django.utils import timezone
<<<<<<< HEAD
 # link to admin dataset
=======
from admins.models import DatasetUpload  # link to admin dataset
>>>>>>> 4e3276bf1ebc3f406edcdefb65dc022f67580260

# --------------------------
# Agent Registration
# --------------------------
class BitAgentRegisterModel(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    pswd = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    pan = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    cryptcurrency = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='waiting')
    authkey = models.CharField(max_length=100, default='waiting')
    cdate = models.DateTimeField()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'agentregister'

    def save(self, *args, **kwargs):
        """On save, set timestamp if new"""
        if not self.id:
            self.cdate = timezone.now()
        return super().save(*args, **kwargs)


# --------------------------
# Agent Coins
# --------------------------
class AgentHadCrypto(models.Model):
    id = models.AutoField(primary_key=True)
    currencyName = models.CharField(max_length=100)
    useremail = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.useremail

    class Meta:
        db_table = "agentscryptoquantity"
        unique_together = ('currencyName', 'useremail',)


# --------------------------
# Agent Buying Crypto
# --------------------------
class AgentBuyCryptoModel(models.Model):
    id = models.AutoField(primary_key=True)
    agentName = models.CharField(max_length=100)
    agentemail = models.CharField(max_length=100)
    currencyname = models.CharField(max_length=100)
    currentprice = models.FloatField()
    quantity = models.IntegerField()
    payableammount = models.FloatField()
    cardnumber = models.CharField(max_length=100)
    nameoncard = models.CharField(max_length=100)
    cardexpiry = models.CharField(max_length=100)
    cvv = models.IntegerField()
    cdate= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'AgentBuyedTransactions'


# --------------------------
# Agent Predictions
# --------------------------
   # ✅ optional, but ensures table name

# agents/models.py
from admins.models import DatasetUpload  # ✅ Correct import

class DatasetUpload(models.Model):
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return self.file.name.split('/')[-1]

    def __str__(self):
        return self.filename

    
from admins.models import DatasetUpload  # ✅ important!

class AgentPredictionModel(models.Model):
    currency_name = models.CharField(max_length=100)
    predicted_value = models.FloatField()
    actual_value = models.FloatField()
    accuracy = models.FloatField()

    # ✅ This now correctly references admin’s DatasetUpload table
    dataset = models.ForeignKey(DatasetUpload, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.currency_name

    class Meta:
        db_table = 'agent_predictions'
