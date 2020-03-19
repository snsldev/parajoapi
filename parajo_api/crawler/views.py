from django.http import HttpResponse, JsonResponse
from .search.service import searchFromEncar


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def search(request, company, model, modelDetail):

    result = searchFromEncar(company, model, modelDetail)
    return JsonResponse(result, json_dumps_params = {'ensure_ascii': True})