import email
import os 
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings.dev")
django.setup()

from myapp.models import CustomUser, Talk

fakegen = Faker(["ja_JP"])

def create_users(n):
    users = [
        CustomUser(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    CustomUser.objects.bulk_create(users, ignore_conflicts=True)

    my_id = CustomUser.objects.get(username="admin").id

    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id", flat=True)

    talks = []

    for _ in range(len(user_ids)):
        senddesu = Talk(
            sender_id = my_id,
            receiver_id=random.choice(user_ids),
            message=fakegen.text(),
        )
        receivedesu = Talk(
            sender_id=random.choice(user_ids),
            receiver_id=my_id,
            message=fakegen.text(),
        )
        talks.extend([senddesu, receivedesu])
    Talk.objects.bulk_create(talks, ignore_conflicts=True)

    talks = Talk.objects.order_by("-time")[: 2 * len(user_ids)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, fields=["time"])

if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(1000)
    print("done")