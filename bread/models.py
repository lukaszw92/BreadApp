from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Bread(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    water = models.IntegerField()
    salt = models.IntegerField()
    flour_mix = models.ManyToManyField('Flour', through='FlourInBread')
    leaven = models.ForeignKey('Leaven', on_delete=models.CASCADE)

    first_proofing = models.DurationField(null=True, blank=True)
    second_proofing = models.DurationField(null=True, blank=True)
    baking_time = models.DurationField()
    baking_temperature = models.IntegerField()

    rating = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))), unique=True)  # change to choice field
    notes = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


    ## klucz obcy do usera aby każdy user miał swoje chleby

    #    def get_bread_weight(self):
    # get_bread_hydration(self):

#NOT WORKING

    # def get_bread_mass(self):
    #     water = self.water
    #     salt = self.salt
    #     flours = self.flour_mix.all()
    #     flour_masses = []
    #     for flour in flours:
    #         flour = int(flour)
    #         flour_masses.append(flour)
    #     return sum(flour_masses) + int(water) + int(salt)

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
    proofing = models.DurationField(null=True)

    #flour in leaven set

    def __str__(self):
        return f'{self.name}'

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


#   def get_leaven_weight(self):


class FlourInBread(models.Model):
    flour = models.ForeignKey(Flour, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    grams = models.IntegerField()

    def __str__(self):
        return f'{self.flour} | {self.grams}g'








