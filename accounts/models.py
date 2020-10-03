from django.contrib.auth.models import User

def total_users():
    total = 0
    for user in User.objects.all():
        total += 1
    return total
