import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Schedule, BookingRecord

from .models import User


@login_required
def profile(request):
    user = request.user
    records = []

    # get all the booking records for the current user.
    user_booking_records = BookingRecord.objects.filter(user=user)

    # iterate the queryset for adding a `cancelling_url` for each record.
    for user_booking_record in user_booking_records:
        data = dict()
        if user_booking_record.transport_type == "Bus":
            data["data"] = user_booking_record
            data["cancelling_url"] = f"/cancel_now/?departure={user_booking_record.departure}&destination={user_booking_record.destination}&transport_type={user_booking_record.transport_type}&date={user_booking_record.date}&time_id={json.loads(user_booking_record.json_identifier)['time_id']}"
            records.append(data)

    context = {
        "user": user,
        "records": records
    }
    return render(request, "users/profile.html", context)
