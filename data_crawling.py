import os
import requests
import pandas as pd
import asyncio
import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

name_selector = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-corp > a'
title_selector = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-information > div > a'
history_selector = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-information > ul.chip-information-group'

# def get_company_url(links):
#     result_list = []
#     for l in links:
#         res = requests.get(l , headers={"user-agent":user_agent})
#         if res.status_code == 200:
#             soup = BeautifulSoup(res.text, "lxml")
#             name_list = soup.select(name_selector)
            
#             for name in name_list:
#                 link = name.get("href")
#                 result_list.append('https://www.jobkorea.co.kr/'+link)
#         else:
#             raise Exception(f"요청 실패. 응답코드: {res.status_code}")
    
#     return result_list

async def get_company_info(url, session):
    async with session.get(url) as res:
        result_list = []
        if res.status == 200:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            name = soup.select(name_selector).get_text() 
            title = soup.select(title_selector).get_text()
            history = soup.select(history_selector).get_text()
            result_list = [name , title , history]
        else:
            raise Exception(f"요청 실패. 응답코드: {res.status_code}")
    
            
            

async def main(links):
    async with aiohttp.ClientSession(headers={"user-agent":user_agent}) as session:

        result = await asyncio.gather(*[get_company_info(url, session) for url in links])

    return result

if __name__ == '__main__':
    question = input("궁금하신 직무를 입력하세요 : ")
    pages = [f'https://www.jobkorea.co.kr/Search/?stext={question}&tabType=recruit&Page_No='+ str(x) for x in range(1,11)]
    # pages_link = get_company_url(pages)
    pages_data = asyncio.run(main(pages))
    info_df = pd.DataFrame(pages_data)

    d = datetime.now().strftime("%Y-%m-%d")

    info_file_path = f"Datas/{d}.csv"
    info_df.to_csv(info_file_path, index=False)