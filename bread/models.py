from django.db import models
from django.urls import reverse


class Bread(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    water = models.IntegerField()
    salt = models.IntegerField()
    flour_mix = models.ManyToManyField('Flour', through='FlourInBread')
    leaven = models.ForeignKey('Leaven', on_delete=models.CASCADE)

    first_proofing = models.TimeField(null=True)
    second_proofing = models.TimeField(null=True)
    baking_time = models.TimeField()

    rating = models.IntegerField()  # change to choice field
    notes = models.TextField(null=True)

    ## klucz obcy do usera aby każdy user miał swoje chleby

#    def get_bread_weight(self):
# get_bread_hydration(self):


class Grain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_delete_url(self):
        return reverse('remove_grain', args=(self.pk,))


class Flour(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, null=True)
    grain = models.ForeignKey(Grain, on_delete=models.SET_NULL, null=True)
    wholegrain = models.BooleanField(default=False)
    type = models.IntegerField(null=True)

    def get_delete_url(self):
        return reverse('remove_flour', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit_flour', args=(self.pk,))

    def __str__(self):
        return f'{self.name} | {self.brand}'

class Leaven(models.Model):
    name = models.CharField(max_length=100)
    sourdough = models.IntegerField()
    water = models.IntegerField()
    flour = models.ManyToManyField('Flour', through='FlourInLeaven')
    proofing = models.TimeField(null=True)


    def get_delete_url(self):
        return reverse('remove_leaven', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit_leaven', args=(self.pk,))




#   def get_leaven_weight(self):


class FlourInBread(models.Model):
    flour = models.ForeignKey(Flour, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    grams = models.IntegerField()


class FlourInLeaven(models.Model):
    flour = models.ForeignKey(Flour, on_delete=models.CASCADE)
    leaven = models.ForeignKey(Leaven, on_delete=models.CASCADE)
    grams = models.IntegerField()





