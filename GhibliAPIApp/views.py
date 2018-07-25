import json
from collections import defaultdict

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from memoize import memoize
import urllib
import urllib.request, json

REMOVABLE_FIELDS = {'people', 'locations', 'species', 'vehicles', 'url', 'id'}
REMOVABLE_PEOPLE_FIELDS = {'films', 'id', 'species', 'url'}

def data_producer(request):
    all_data = {}
    with urllib.request.urlopen("https://ghibliapi.herokuapp.com/people") as people_url:
        all_peoples = json.loads(people_url.read().decode())
        for people in all_peoples:
            for url in people['films']:
                with urllib.request.urlopen(url) as film_url:
                    film_info = json.loads(film_url.read().decode())

                    filtered_people = {k: v for k, v in people.items() if
                                       k not in REMOVABLE_PEOPLE_FIELDS}

                    filtered_film_info = {k: v for k, v in film_info.items() if
                                       k not in REMOVABLE_FIELDS}

                    if url not in all_data:
                        all_data[url] = filtered_film_info
                    if 'peoples' not in all_data[url]:
                        all_data[url]['peoples'] = [filtered_people]
                    else:
                        if filtered_people not in all_data[url]['peoples']:
                            all_data[url]['peoples'].append(filtered_people)

    all_data = [v for k, v in all_data.items()]
    return all_data



@memoize(timeout=60)
def get_all_movies(request):
    all_data = data_producer(request)
    return render(request, 'movies.html', {'all_data': all_data})