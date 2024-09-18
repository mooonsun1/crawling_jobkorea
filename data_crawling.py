import os
import requests
import pandas as pd
import asyncio
import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

company_name = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-corp > a'
company_title = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-information > div > a'
personal_history = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-information > ul.chip-information-group'

def get_company_url(links):
    pass

async def get_company_info(url, session):
    pass

async def main(links):
    pass

if __name__ == '__main__':
    question = input("궁금하신 직무를 입력하세요 : ")
    pages = [f'https://www.jobkorea.co.kr/Search/?stext={question}&tabType=recruit&Page_No='+ str(x) for x in range(1,11)]
    pages_link = get_company_url(pages)
    pages_data = asyncio.run(main(pages_link))
    info_df = pd.DataFrame(pages_data)

    d = datetime.now().strftime("%Y-%m-%d")
