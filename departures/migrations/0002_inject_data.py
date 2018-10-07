# Generated by Django 2.0.2 on 2018-10-05 21:51

input_file = "departures.json"

from django.db import migrations
import json


def construct_departure_list(departure_json_list, Departure):
    '''
    Format the json list representing Departure objects into an list of Departure objects.
    Return a Departure object list.
    '''
    departure_object_list = []
    for departure in departure_json_list:
        new_departure = Departure(
            name=departure["name"],
            start_date=departure["start_date"],
            finish_date=departure["finish_date"],
            category=departure["category"]
        )
        departure_object_list.append(new_departure)
    return departure_object_list


def inject_departures(apps, schema_editor):
    '''
    Opens the departures.json file which contains json data representing Departure objects.
    The script then formats the json data, and inserts the formatted data into the database.
    '''
    input_departures_json_string = open('departures.json').read()
    departure_json_list = json.loads(input_departures_json_string)
    Departure = apps.get_model("departures", "Departure")
    departure_object_list = construct_departure_list(
        departure_json_list, Departure)
    db_alias = schema_editor.connection.alias
    # Use bulk_create to save on db queries.
    Departure.objects.using(db_alias).bulk_create(departure_object_list)


class Migration(migrations.Migration):

    dependencies = [
        ('departures', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(inject_departures),
    ]
