from django.http import HttpResponse, JsonResponse
from .search.service import searchFromEncar


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def search(request, company, model, modelDetail):

    result={
        'status': '',
        'result': ''
    }
    contentList = searchFromEncar(company, model, modelDetail)
    if contentList is None:
        result['status'] = 'error'
    elif len(contentList) == 0:
        result['status'] = 'empty'
    else:
        result['status'] = 'success'
        result['result'] = contentList

    return JsonResponse(result, safe=False)