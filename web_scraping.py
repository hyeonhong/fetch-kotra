# -*- coding: utf-8 -*-
import sys
import re
import time
import requests
from bs4 import BeautifulSoup
from googletrans import Translator


def build_list(country):
    pre_oid = r'http://www.ois.go.kr/portal/page?_pageid=93,738903&_dad=portal&_schema=PORTAL&p_deps1=pds&p_deps2=&searchopt1=&searchword1=&oid='
    pre_page_number = r'http://news.kotra.or.kr/user/overseasCompany/kotranews/29/usrOverseasCompanyList.do?searchGbn=1&searchDimNation={0}&page='
    pre_page_number = pre_page_number.format(translate_to_kr(country))
    page_number = 1
    url_list = []

    while True:
        listing_url = pre_page_number + str(page_number)
        print("Scraping addresses on page " + str(page_number))
        try:
            response = requests.get(listing_url)
        except requests.exceptions.RequestException as e:
            # print(e)
            print("HTTP Connection Error - we will try to connect again")

        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.find(class_='al bbsTitle') is None:
            break

        for tag in soup.find_all(class_='al bbsTitle'):
            oid = re.findall('\d+', tag.a['href'])[-1]
            url_list.append(pre_oid + oid)
            print(pre_oid + oid)

        page_number += 1

        # # for testing
        # break


    return url_list


def scrape(url_list, entry_list):
    items = [
        "진출국가",
        "진출지역",
        "회사명(국문)",
        "회사명(영문)",
        "주소",
        "전화",
        "팩스",
        "해외대표",
        "이메일",
        "진출년도",
        "진출형태",
        "투자형태",
        "홈페이지",
        "업종(대)",
        "업종(중)",
        "취급분야",
        "종업원(한국)",
        "종업원(외국)",
        "내수/수출",
        "대상고객",
        "모기업명",
        "모기업주소",
        "모기업전화번호"
    ]

    remaining_url_list = []

    for url in url_list:
        remaining_url_list.append(url)
        try:
            time.sleep(1.5)
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            # print(e)
            print("HTTP Connection Error - we will try to connect again")
            continue

        remaining_url_list.pop()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape the contents inside the table and put them into entry{}
        i = 0
        entry = {}

        # Capture the contents by matching the color "#FFFFFF" in the webpage
        # Beware of the possible color change in the future!
        # To be safe, we can capture the outer table first, and then capture the color inside like the code below.
        # outer_table = soup.find(id="idPrint")
        # table = outer_table.find(bgcolor='#E8E8E8')
        table = soup.find(bgcolor='#E8E8E8')
        for tag in table.find_all(bgcolor='#FFFFFF'):
            entry[items[i]] = tag.get_text()
            i = i + 1  # Assumption - only 23 items per table. Otherwise, out-of-bounds error may occur.

        entry_list.append(entry)
        print("Scraping complete for URL with oId=", url[-19:])

    return remaining_url_list


def translate_to_kr(region):
    response = requests.get('http://news.kotra.or.kr/user/overseasCompany/kotranews/29/usrOverseasCompanyList.do')
    soup = BeautifulSoup(response.text, 'html.parser')

    print("Checking the argument for region...")

    # Build the country_list_kr
    country_list_kr = []
    table = soup.find(id='searchDimNation')
    for tag in table.find_all('option'):
        country_list_kr.append(tag.get_text())
    country_list_kr.pop(0)
    country_list_kr.remove('농림·수산업·임업')

    # print(country_list_kr)

    # Build the en_to_kr_dictionary
    en_to_kr_dictionary = {}
    translator = Translator()
    for country in country_list_kr:
        result = translator.translate(country, dest='en')
        en_to_kr_dictionary[result.text] = country

    if region in en_to_kr_dictionary.keys():
        return en_to_kr_dictionary[region]
    else:
        print("Error: unrecognized argument for region./n")
        sys.exit(1)
