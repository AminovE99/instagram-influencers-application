from django.shortcuts import render

# Create your views here.
from webscrape_app.webscrape_util import instascrape


def search_by_tag_view(request):
    if request.POST:
        data = request.POST.get('search_hashtag')
        instascrape.instascrape.delay(
            "/home/emil/Desktop/instagram_influencers_application/webscrape_app/data/influenc_d.json", 10, data)
    return render(request, "input_page.html")
