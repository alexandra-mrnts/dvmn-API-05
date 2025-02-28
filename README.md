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


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
