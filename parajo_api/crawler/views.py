from django.http import HttpResponse, JsonResponse
from .scrap.ScrapService import ScrapService

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def scrapCarInfo(request):
    scrapService = ScrapService()
    scrapService.scrapCarInfo()
    return HttpResponse("crawling scrapCarInfo success!")

def scrapCarGrade(request):
    scrapService = ScrapService()
    scrapService.scrapCarGrade()
    return HttpResponse("crawling scrapCarGrade success!")

# def search(request, company, model, modelDetail):

#     result={
#         'status': '',
#         'result': ''
#     }
#     contentList = searchFromEncar(company, model, modelDetail)
#     if contentList is None:
#         result['status'] = 'error'
#     elif len(contentList) == 0:
#         result['status'] = 'empty'
#     else:
#         result['status'] = 'success'
#         result['result'] = contentList

#     return JsonResponse(result, safe=False)