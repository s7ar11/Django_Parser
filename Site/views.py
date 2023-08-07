# parser_app/views.py

import re
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def parse_url(request):
    base_url = 'http://example.com/parser/'  # Задайте здесь базовый URL по умолчанию
    start_page = 1
    end_page = 1
    result = []

    if request.method == 'POST':
        base_url = request.POST.get('base_url', base_url)
        start_page = int(request.POST.get('start_page', start_page))
        end_page = int(request.POST.get('end_page', end_page))
        output_file = 'broken_images.txt'

        num_links_found = 0

        for i in range(start_page, end_page + 1):
            url = base_url.format(i)
            try:
                response = requests.get(url)
            except requests.exceptions.RequestException:
                continue
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            images = soup.find_all('img')

            for image in images:
                src = image.get('src')
                if not src:
                    continue
                if src.startswith('http'):
                    image_url = src
                else:
                    base_domain = re.search("(https?://.*?)/", url).group(1)
                    image_url = base_domain + src if src.startswith("/") else base_domain + '/' + src
                try:
                    response = requests.get(image_url)
                except requests.exceptions.RequestException:
                    continue
                if response.status_code != 200:
                    matching_link = f"{url} >> {image_url}"
                    result.append(matching_link)
                    num_links_found += 1

        # После выполнения парсинга, автоматически перенаправляем пользователя на страницу с результатами
        return redirect(reverse('result_page'))

    return render(request, 'index.html', {'base_url': base_url, 'start_page': start_page, 'end_page': end_page, 'result': result})

def result_page(request):
    # В представлении result_page вы можете снова выполнить парсинг, если необходимо,
    # или просто отобразить результаты, которые уже были получены в представлении parse_url.
    # В данном примере просто передадим данные в шаблон result.html.
    return render(request, 'result.html')
