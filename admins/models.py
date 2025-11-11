from django.db import models
from django.utils import timezone
import os





def dataset_file_path(instance, filename):
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    basename, ext = os.path.splitext(filename)
    return f'datasets/{timestamp}_{basename}{ext}'

class cryptcurrencyratemodel(models.Model):
    currencytype=models.CharField(max_length=100, null=True, blank=True)
    doller=models.FloatField()
    rupee=models.FloatField()
    originalprice = models.FloatField()

    def __str__(self):
        return self.currencytype
    class Meta:
        db_table = 'currencyrate'

class CurrencyUpdateModel(models.Model):
    id = models.AutoField(primary_key=True)
    currencyname = models.CharField(max_length=100)
    conversionRate = models.FloatField()
    newCurrencyValue = models.FloatField()
    originalCurrencyValue = models.FloatField()
    chnageValue = models.FloatField()
    profitorloss = models.CharField(max_length=50)
    changedate = models.DateTimeField()

    def __str__(self):
        return self.currencyname
    class Meta:
        db_table = 'currencychnagetable'
        unique_together = ('currencyname', 'changedate',)


class DatasetUpload(models.Model):
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        # returns just the file name from file path
        return self.file.name.split('/')[-1]

    def __str__(self):
        return self.filename

