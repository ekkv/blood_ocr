<a name="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">О проекте</a></li>
    <li><a href="#built-with">Используемые библиотеки</a></li>
    <li><a href="#installation">Установка</a></li>
    <li><a href="#usage">Применение</a></li>
  </ol>
</details>


<a name="about-the-project"></a>
## О проекте

Страница OCR-решения для общества доноров крови “DonorSearch”. Алгоритм автоматического распознавания текста из табличных данных с фотографий справок. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="built-with"></a>
### Используемые библиотеки

- EasyOCR
- Opencv-python
- Pandas
- FastAPI
- Uvicorn
- Celery

Для бэкенда используется docker-образ Redis:alpine

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="usage"></a>
## Применение
1) git clone https://github.com/ekkv/donation_ocr.git
2) cmd: cd donation_ocr
3) cmd: docker compose up
4) Пример запроса: curl -X POST -F file=@file.jpg http://localhost:8000/ocr/upload

<p align="right">(<a href="#readme-top">back to top</a>)</p>
