from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


def positive_validator(value):
    if value <= 0:
        raise ValidationError("Value has to be greater than 0.")


def non_negative_validator(value):
    if value < 0:
        raise ValidationError("Value cannot be negative.")

def no_negative_duration(value):
    days = value.days
    seconds = value.seconds
    if 24*3600*days + seconds <= 0:
        raise ValidationError("Baking/proofing time cannot be negative.")


class Bread(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    water = models.IntegerField(validators=[positive_validator])
    salt = models.IntegerField(validators=[non_negative_validator])
    flour_mix = models.ManyToManyField('Flour', through='FlourInBread')
    leaven = models.ForeignKey('Leaven', on_delete=models.CASCADE)

    first_proofing = models.DurationField(null=True, blank=True)
    second_proofing = models.DurationField(null=True, blank=True)
    baking_time = models.DurationField(validators=[no_negative_duration])
    baking_temperature = models.IntegerField(validators=[positive_validator])

    rating = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))))
    notes = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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
        return f'{round(water / flours_weight * 100)}%'

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
    type = models.IntegerField(null=True, validators=[non_negative_validator])

    def get_delete_url(self):
        return reverse('remove_flour', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit_flour', args=(self.pk,))

    def __str__(self):
        return f'{self.name} | {self.brand}'


class Leaven(models.Model):
    name = models.CharField(max_length=100)
    sourdough = models.IntegerField(validators=[positive_validator])
    water = models.IntegerField(validators=[positive_validator])
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
    grams = models.IntegerField(null=True, validators=[positive_validator])

    def __str__(self):
        return f'{self.flour} | {self.grams}g'

    def get_delete_url(self):
        return reverse('remove_flour_leaven', args=(self.pk,))


class FlourInBread(models.Model):
    flour = models.ForeignKey(Flour, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    grams = models.IntegerField(null=True, validators=[positive_validator])

    def __str__(self):
        return f'{self.flour} | {self.grams}g'

    def get_delete_url(self):
        return reverse('remove_flour_bread', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit_flour_bread', args=(self.pk,))
