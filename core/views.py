from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def get_html(request):
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content

def home(request):
    #fetch data
    data = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content = get_html(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        data = dict()
        data['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        data['time_now'] = soup.find("div", attrs={"id": "wob_dts"}).text
        data['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
        data['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        return render(request, 'core/home.html', {'data': data})
    return render(request, 'core/home.html')