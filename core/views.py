import datetime
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import formats

import requests
from bs4 import BeautifulSoup

from .models import Schedule, BookingRecord
from .forms import ContactForm
from .constants import BILAL_TRAVELS_DATA


def index(request):
    context = {
        "hide_navbar_brand": True
    }
    return render(request, "core/index.html", context)


def offers(request):
    return render(request, "core/offers.html")


def companies(request):
    return render(request, "core/companies.html")


def feedback(request):
    return render(request, "core/feedback.html")


def hotels(request):
    context = {
        "navbar_brand_text": "Adventure",
        "toggle_the_navbar": True
    }
    return render(request, "core/hotels.html", context)


def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 "Your message has been sent successfully.")
            return redirect("/")

    return render(request, "core/contact.html")


def blog(request):
    context = {
        "navbar_brand_text": "Adventure",
        "toggle_the_navbar": True
    }
    return render(request, "core/blog.html", context)


def single_blog(request, slug):
    context = {
        "navbar_brand_text": "Adventure",
        "toggle_the_navbar": True
    }
    return render(request, "core/single_blog.html", context)


def schedules(request):
    departure = request.GET.get('departure', '')
    destination = request.GET.get('destination', '')
    transport_type = request.GET.get('transport_type', '')
    date = request.GET.get('date', '')

    if transport_type == "Bus":
        url_for_booking = f"/book_now/?departure={departure}&destination={destination}&transport_type={transport_type}&date={date}&time_id="

        # Check database against the required data.
        db_schedules = Schedule.objects.filter(
            departure=departure,
            destination=destination,
            transport_type=transport_type,
            date=date
        )
        if db_schedules.exists():
            schedules = json.loads(db_schedules[0].json_data)

        else:
            # Get city ids for departure & destination for bilal travels only.
            for city_id, city_name in BILAL_TRAVELS_DATA.items():
                if city_name == departure:
                    departure_city_id = city_id
                if city_name == destination:
                    destination_city_id = city_id

            # Format the date for bilal travels only.
            date_obj = datetime.datetime.strptime(date, "%m/%d/%Y").date()
            formatted_date = formats.date_format(date_obj, "Y-m-d")

            url = f"http://bilaltravel.pk/bus/times?dep={departure_city_id}&arr={destination_city_id}&date={formatted_date}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            panels = soup.findAll(attrs={"class": "panel-heading panel-heading--api"})

            schedules = []
            for panel in panels:
                data = dict()
                data["start"] = panel.find(attrs={"class": "routes-list__info routes-list__start"}).find('span', {"class": "time"}).text
                data["duration"] = panel.find(attrs={"class": "routes-list__info routes-list__duration"}).find('span').text
                data["finish"] = panel.find(attrs={"class": "routes-list__info routes-list__finish"}).find('span').text
                data["bus"] = panel.find(attrs={"class": "routes-list__info routes-list__extra routes-list__extra--1"}).find('p').text
                data["price"] = panel.find(attrs={"class": "routes-list__info routes-list__price"}).find('span', {"class": "route-price-amount"}).text
                data["time_id"] = panel.find('input', {"name": "time_id"})['value']
                schedules.append(data)

            if len(schedules) > 0:
                Schedule.objects.create(
                    departure=departure,
                    destination=destination,
                    transport_type=transport_type,
                    date=date,
                    json_data=json.dumps(schedules)
                )

    else:
        pass

    context = {
        "hide_navbar_brand": True,
        "transport_type": transport_type,
        "schedules": schedules or [],
        "url_for_booking": url_for_booking or ''
    }
    return render(request, "core/schedules.html", context)


def book_now(request):
    departure = request.GET.get('departure', '')
    destination = request.GET.get('destination', '')
    transport_type = request.GET.get('transport_type', '')
    date = request.GET.get('date', '')
    time_id = request.GET.get('time_id', '')

    if transport_type == "Bus":

        # Get city ids for departure & destination for bilal travels only.
        for city_id, city_name in BILAL_TRAVELS_DATA.items():
            if city_name == departure:
                departure_city_id = city_id
            if city_name == destination:
                destination_city_id = city_id

        # Format the date for bilal travels only.
        date_obj = datetime.datetime.strptime(date, "%m/%d/%Y").date()
        formatted_date = formats.date_format(date_obj, "Y-m-d")

        if request.user.is_authenticated:
            BookingRecord.objects.create(
                user=request.user,
                departure=departure,
                destination=destination,
                transport_type=transport_type,
                date=date,
                json_identifier=json.dumps({"time_id": time_id})
            )

        url_for_booking = f"http://bilaltravel.pk/bus/nextstep/{departure_city_id}/{destination_city_id}/{formatted_date}"
        response = requests.post(url_for_booking, data={"time_id": time_id})
        return redirect(response.url)

    return redirect("/")


def cancel_now(request):
    departure = request.GET.get('departure', '')
    destination = request.GET.get('destination', '')
    transport_type = request.GET.get('transport_type', '')
    date = request.GET.get('date', '')
    time_id = request.GET.get('time_id', '')

    if transport_type == "Bus":

        # Get city ids for departure & destination for bilal travels only.
        for city_id, city_name in BILAL_TRAVELS_DATA.items():
            if city_name == departure:
                departure_city_id = city_id
            if city_name == destination:
                destination_city_id = city_id

        # Format the date for bilal travels only.
        date_obj = datetime.datetime.strptime(date, "%m/%d/%Y").date()
        formatted_date = formats.date_format(date_obj, "Y-m-d")

        if request.user.is_authenticated:
            booking_record = BookingRecord.objects.filter(
                user=request.user,
                departure=departure,
                destination=destination,
                transport_type=transport_type,
                date=date
            ).first()
            booking_record.delete()

        url_for_booking = f"http://bilaltravel.pk/bus/nextstep/{departure_city_id}/{destination_city_id}/{formatted_date}"
        response = requests.post(url_for_booking, data={"time_id": time_id})
        return redirect(response.url)

    return redirect("/")
