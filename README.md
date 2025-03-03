# Programming vacancies compare

The script compares number of vacancies and average salaries for engineers specializing in top programming languages.   
Data is sourced from job postings on [HeadHunter](https://hh.ru) and [SuperJob](https://www.superjob.ru) for the Moscow region over the past 30 days. 

### How to install

Python3 should already be installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Your SuperJob secret key should be added to the .env file.
```
SUPERJOB_SECRET_KEY = 'v3.r.138926438.d8028b0d71e50b993d0ea4099c0633000a5d68fb.b9ecc3f0ab9dee0b87295d1b80b1d5fe4e8cdfad' 
```
You can generate your secret key here: https://api.superjob.ru/

### How to use
```
% python3 main.py  

┌HeadHunter Москва──────────────┬─────────────────────┬───────────────────────┐
│ Язык       │ Вакансий найдено │ Вакансий обработано │ Средняя зарплата, руб │
├────────────┼──────────────────┼─────────────────────┼───────────────────────┤
│ JavaScript │ 266              │ 92                  │ 217933                │
│ Java       │ 426              │ 66                  │ 231135                │
│ Python     │ 393              │ 100                 │ 219904                │
│ Ruby       │ 20               │ 5                   │ 221000                │
│ PHP        │ 388              │ 169                 │ 194154                │
│ C++        │ 391              │ 102                 │ 241467                │
│ C#         │ 254              │ 67                  │ 236820                │
│ C          │ 93               │ 24                  │ 242395                │
│ Go         │ 187              │ 19                  │ 325868                │
└────────────┴──────────────────┴─────────────────────┴───────────────────────┘
┌SuperJob Москва────────────────┬─────────────────────┬───────────────────────┐
│ Язык       │ Вакансий найдено │ Вакансий обработано │ Средняя зарплата, руб │
├────────────┼──────────────────┼─────────────────────┼───────────────────────┤
│ JavaScript │ 5                │ 2                   │ 145000                │
│ Java       │ 2                │ 0                   │                       │
│ Python     │ 1                │ 1                   │ 203500                │
│ Ruby       │ 0                │ 0                   │                       │
│ PHP        │ 3                │ 2                   │ 127000                │
│ C++        │ 4                │ 3                   │ 198000                │
│ C#         │ 1                │ 1                   │ 237500                │
│ C          │ 2                │ 2                   │ 192000                │
│ Go         │ 2                │ 0                   │                       │
└────────────┴──────────────────┴─────────────────────┴───────────────────────┘
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
