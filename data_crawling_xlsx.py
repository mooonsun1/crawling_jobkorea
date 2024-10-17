import pandas as pd
import asyncio
import aiohttp
import openpyxl 
from datetime import datetime
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

name_selector = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-corp > a'
title_selector = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-information > div > a'
history_selector = '#dev-content-wrap > article > section.content-recruit.on > article.list > article > div.list-section-information > ul.chip-information-group'

async def get_company_info(url, session):
    async with session.get(url) as res:
        all_results = []
        if res.status == 200:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")

            name_list = soup.select(name_selector)
            title_list = soup.select(title_selector)
            history_list = soup.select(history_selector)

            name = [n.get_text().strip() for n in name_list]
            title = [t.get_text().strip() for t in title_list]
            history = [h.get_text().strip().replace('\n','') for h in history_list]
            
            result_list = list(zip(name , title , history))
            all_results.extend(result_list)
            return all_results
        else:
            raise Exception(f"요청 실패. 응답코드: {res.status_code}")
    
            
            

async def main(links):
    async with aiohttp.ClientSession(headers={"user-agent":user_agent}) as session:

        result = await asyncio.gather(*[get_company_info(url, session) for url in links])

    return result

if __name__ == '__main__':
    question = input("궁금하신 직무를 입력하세요 : ")
    pages = [f'https://www.jobkorea.co.kr/Search/?stext={question}&tabType=recruit&Page_No='+ str(x) for x in range(1,11)]

    pages_data = asyncio.run(main(pages))
    
    

    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = f"{question} 직무 채용 공고"
    sheet.append(['회사명', '직무명' , '상세정보'])
    sheet.column_dimensions['A'].width = 30
    sheet.column_dimensions['B'].width = 80
    sheet.column_dimensions['C'].width = 60
    [sheet.append(item) for subdata in pages_data for item in subdata]
    
    d = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    excel.save(f'{d}.xlsx')