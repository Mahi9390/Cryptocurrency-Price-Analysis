from django.db import models
from django.utils import timezone
from admins.models import DatasetUpload   # ✅ Correct import



  # link to admin dataset

# --------------------------
# User Registration
# --------------------------
class BitUserRegisterModel(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    pswd = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    pan = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='waiting')
    authkey = models.CharField(max_length=100, default='waiting')
    cdate = models.DateTimeField()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'userregister'

    def save(self, *args, **kwargs):
        """On save, set timestamp if new"""
        if not self.id:
            self.cdate = timezone.now()
        return super().save(*args, **kwargs)


# --------------------------
# Customer Coins
# --------------------------
class CustomerHadCoins(models.Model):
    id = models.AutoField(primary_key=True)
    currencyName = models.CharField(max_length=100)
    customeremail = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.customeremail

    class Meta:
        db_table = "CustomerContainCoins"
        unique_together = ('currencyName', 'customeremail',)


# --------------------------
# User Buying Crypto
# --------------------------
class UserBuyingCryptoModel(models.Model):
    id = models.AutoField(primary_key=True)
    customername = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    currencyname = models.CharField(max_length=100)
    quantity = models.IntegerField()
    agentemail = models.CharField(max_length=100)
    singlecoingamount = models.FloatField()
    payableammount = models.FloatField()
    cardnumber = models.CharField(max_length=100)
    nameoncard = models.CharField(max_length=100)
    cardexpiry = models.CharField(max_length=100)
    cvv = models.IntegerField()
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'UserBuyingCryptoModel'


# --------------------------
# Blockchain Ledger
# --------------------------
class BlockChainLedger(models.Model):
    id = models.AutoField(primary_key=True)
    customeremail = models.CharField(max_length=100)
    agentemail = models.CharField(max_length=100)
    currencyname = models.CharField(max_length=100)
    quantity = models.IntegerField()
    paidammout = models.FloatField()
    blockchainmoney = models.FloatField()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "BlockChainLedger"


# --------------------------
# User Predictions
# --------------------------

class DatasetUpload(models.Model):
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        # returns just the file name from file path
        return self.file.name.split('/')[-1]

    def __str__(self):
        return self.filename




class UserPredictionModel(models.Model):
    currency_name = models.CharField(max_length=100)
    predicted_value = models.FloatField()
    actual_value = models.FloatField()
    accuracy = models.FloatField()

    # Link to dataset uploaded by admin
    dataset = models.ForeignKey(DatasetUpload, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.currency_name

    class Meta:
        db_table = 'user_predictions'
