from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Bread(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    water = models.IntegerField()
    salt = models.IntegerField()
    flour_mix = models.ManyToManyField('Flour', through='FlourInBread')
    leaven = models.ForeignKey('Leaven', on_delete=models.CASCADE)  # FIX this should be in leaven

    first_proofing = models.DurationField(null=True, blank=True)
    second_proofing = models.DurationField(null=True, blank=True)
    baking_time = models.DurationField()
    baking_temperature = models.IntegerField()

    rating = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))), unique=True)  # change to choice field
    notes = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_total_flour_weight(self):
        flours = self.flourinbread_set.all()
        weights = []
        for flour in flours:
            weights.append(flour.grams)
        return sum(weights)

    def weight(self):
        water = self.water
        salt = self.salt
        flours_weight = self.get_total_flour_weight()
        leaven_weight = self.leaven.leaven_weight()
        return water + salt + flours_weight + leaven_weight

    def hydration(self):
        water = self.water
        flours_weight = self.get_total_flour_weight()
        if flours_weight == 0:
            return "n/a"
        return f'{water / flours_weight * 100}%'

    def __str__(self):
        return f'{self.name}'

    def get_delete_url(self):
        return reverse('remove_bread', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit_bread', args=(self.pk,))

    def get_flour_list(self):
        return self.flourinbread_set.all()

    def get_add_flour_url(self):
        return reverse('flour_in_bread', args=(self.pk,))


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
    flour = models.ManyToManyField(Flour, through='FlourInLeaven')
    proofing = models.DurationField(null=True, verbose_name="Fermentation")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'{self.name}'

    def get_total_flour_weight(self):
        flours = self.flourinleaven_set.all()
        weights = []
        for flour in flours:
            weights.append(flour.grams)
        return sum(weights)

    def leaven_weight(self):
        water = self.water
        sourdough = self.sourdough
        flours_weight = self.get_total_flour_weight()
        return water + sourdough + flours_weight

    def get_delete_url(self):
        return reverse('remove_leaven', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit_leaven', args=(self.pk,))

    def get_flour_list(self):
        return self.flourinleaven_set.all()

    def get_add_flour_url(self):
        return reverse('flour_in_leaven', args=(self.pk,))


class FlourInLeaven(models.Model):
    flour = models.ForeignKey(Flour, on_delete=models.CASCADE)
    leaven = models.ForeignKey(Leaven, on_delete=models.CASCADE)
    grams = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.flour} | {self.grams}g'


class FlourInBread(models.Model):
    flour = models.ForeignKey(Flour, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    grams = models.IntegerField()

    def __str__(self):
        return f'{self.flour} | {self.grams}g'
