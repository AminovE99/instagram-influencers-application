from django.shortcuts import render

# Create your views here.
from webscrape_app.webscrape_util import instascrape


from django.http import JsonResponse
from django.shortcuts import render

from webscrape_app.webscrape_util import instascrape
from rest_framework.views import APIView


class SearchByTagView(APIView):
    def get(self, request):
        return render(request, "input_page.html")

    def post(self, request):
        data = request.POST.get('search_hashtag')
        instascrape.instascrape.delay(
            "/home/emil/Desktop/instagram_influencers_application/webscrape_app/data/influenc_d.json", 10, data)

        return JsonResponse(data={'status': 'ok'}, status=200)

