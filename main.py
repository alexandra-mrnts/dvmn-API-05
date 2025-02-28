import os
import requests
import statistics
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from itertools import count
from terminaltables import SingleTable


PROGRAMMING_LANGUAGES = ('JavaScript', 'Java', 'Python', 'Ruby', 'PHP',
                         'C++', 'C#', 'C', 'Go')
TEXT_EXCLUDE_FROM_SEARCH = {'C': '1C'}
DAYS_SINCE_PUBLICATION = 30


def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    if not salary_from:
        predicted_salary = salary_to * 0.8
    elif not salary_to:
        predicted_salary = salary_from * 1.2
    else:
        predicted_salary = statistics.mean((salary_from, salary_to))
    return round(predicted_salary, 0)


def predict_rub_salary_hh(vacancy):
    if not vacancy['salary']:
        return None
    if vacancy['salary']['currency'] != 'RUR':
        return None
    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']
    return predict_salary(salary_from, salary_to)


def predict_rub_salary_superJob(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    if vacancy['payment_from'] == 0:
        salary_from = None
    else:
        salary_from = vacancy['payment_from']
    if vacancy['payment_to'] == 0:
        salary_to = None
    else:
        salary_to = vacancy['payment_to']
    return predict_salary(salary_from, salary_to)


def fetch_vacancies_from_hh(vacancy_name, area_code, period):
    url = 'https://api.hh.ru/vacancies'
    params = {'text': vacancy_name,
              'search_field': 'name',
              'area': area_code,
              'period': period,
              'per_page': 100
              }
    vacancies = []
    for page in count(0):
        params['page'] = page
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        response_body = response.json()
        vacancies += response_body['items']
        if page >= response_body['pages']:
            break
    vacancies_count = response_body['found']
    return vacancies_count, vacancies


def fetch_vacancies_from_superjob(keyword, professional_field_id, town_id,
                                  period, api_key):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': api_key}
    date_published_from = datetime.now() - timedelta(days=period)
    date_published_from_unix = int(date_published_from.timestamp())
    params = {'keyword': keyword,
              'catalogues': professional_field_id,
              'town': town_id,
              'date_published_from': date_published_from_unix,
              'count': 100}
    vacancies = []
    for page in count(0):
        params['page'] = page
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        response_body = response.json()
        vacancies += response_body['objects']
        if not response_body['more']:
            break
    vacancies_count = response_body['total']
    return vacancies_count, vacancies


def get_hh_stats(languages, exlude_from_search, period, area_code):
    vacancies_stats = {}

    for language in languages:
        vacancies_stats[language] = {}
        vacancy_name = f'разработчик {language}'
        if language in exlude_from_search:
            vacancy_name += f' NOT {exlude_from_search[language]}'
        vacancies_found, vacancies = fetch_vacancies_from_hh(
                                        vacancy_name=vacancy_name,
                                        area_code=area_code,
                                        period=period
                                     )
        salaries = []
        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_hh(vacancy)
            if predicted_salary:
                salaries.append(predicted_salary)

        vacancies_stats[language]['vacancies_found'] = vacancies_found
        vacancies_stats[language]['vacancies_processed'] = len(salaries)
        if vacancies_stats[language]['vacancies_processed'] > 0:
            vacancies_stats[language]['average_salary'] = int(statistics.mean(salaries))
    return vacancies_stats


def get_superjob_stats(languages, professional_field_id, period, town_id, api_key):
    vacancies_stats = {}
    for language in languages:
        vacancies_stats[language] = {}
        vacancies_found, vacancies = fetch_vacancies_from_superjob(
                                        keyword=language,
                                        professional_field_id=professional_field_id,
                                        town_id=town_id,
                                        period=period,
                                        api_key=api_key
                                     )
        salaries = []
        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_superJob(vacancy)
            if predicted_salary:
                salaries.append(predicted_salary)
        
        vacancies_stats[language]['vacancies_found'] = vacancies_found
        vacancies_stats[language]['vacancies_processed'] = len(salaries)
        if vacancies_stats[language]['vacancies_processed'] > 0:
            vacancies_stats[language]['average_salary'] = int(statistics.mean(salaries))
    return vacancies_stats


def print_as_table(title, headers, values):
    table_data = []
    table_data.append(headers)
    for item in values:
        table_data.append([item])
        table_data[-1] += list(values[item].values())
    table = SingleTable(table_data, title)
    print(table.table)


def main():
    load_dotenv()

    try:
        hh_vacancies_stats = get_hh_stats(languages=PROGRAMMING_LANGUAGES,
                                          exlude_from_search=TEXT_EXCLUDE_FROM_SEARCH,
                                          period=DAYS_SINCE_PUBLICATION,
                                          area_code=1)
    except HTTPError as err:
        print(f'Ошибка при получении вакансий от hh.ru: {err}')

    superjob_api_key = os.getenv('SUPERJOB_SECRET_KEY')
    try:
        superjob_vacancies_stats = get_superjob_stats(languages=PROGRAMMING_LANGUAGES,
                                                      professional_field_id=48,
                                                      town_id=4,
                                                      period=DAYS_SINCE_PUBLICATION,
                                                      api_key=superjob_api_key)
    except HTTPError as err:
        print(f'Ошибка при получении вакансий от superjob.ru: {err}')

    print_as_table(title='HeadHunter Москва',
                   headers=['Язык', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата, руб'],
                   values=hh_vacancies_stats)
    print_as_table(title='SuperJob Москва',
                   headers=['Язык', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата, руб'],
                   values=superjob_vacancies_stats)


if __name__ == '__main__':
    main()
