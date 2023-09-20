from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from .webscrapper import get_categories, scrape
from .googleapi import populate_gsheet, webhook_response


@csrf_exempt
def the_scrapper(request):
    """
    Esta view se encarga de manejar los request hechos a la API.
    """

    categories = get_categories()

    if request.method == 'POST':
        data = json.loads(request.body)
        category = data.get('category').lower()
        if category in categories.keys():
            if category == 'blog':
                all_contents = []
                for k in categories.keys():
                    if k != 'blog':
                        url = categories[k]
                        content = scrape(url)
                        all_contents += content
                response = populate_gsheet(all_contents)
            else:
                content = scrape(categories[category])
                response = populate_gsheet(content)
            webhook = data.get('webhook')
            webhook_respone = webhook_response(webhook)
            if webhook_respone.status_code != 200:
                return HttpResponseServerError('Connection to webhook failed')
            return HttpResponse('Puedes revisar tu GSheet aquí: https://docs.google.com/spreadsheets/d/1UlsvCxYmEUKC8aSl5WCd2zphNEUKYmUkxrZMR9Ujd1E ')
        else:
            return HttpResponse(f"Esta categoría no esta dentro de las categorías posibles: {', '.join(categories.keys())}", status=400)

    if request.method == 'GET':
        text = ', '.join(categories.keys())
        context = {'categories': text}
        return render(request, 'webscrapper/instructions.html', context=context)

