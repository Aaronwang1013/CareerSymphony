from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import random

user_agent_list = [ "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                                                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                                                "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                                                "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                                                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                                                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                                                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                                                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                                                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                                                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                                                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                                                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
                                                "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
                                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
                                                "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
                                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
                                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
                                                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
                                                ]
class Query(ABC):
    def __init__(self , Jobtitle , page):
        self.Jobtitle = Jobtitle
        self.page = page
    @abstractmethod
    def scrape(self):
        pass

## 執行搜尋-> 抓資料下來後寸入資料庫並進行視覺化 -> 下次若搜尋相同關鍵字，直接從資料庫找
class JobQuery(Query):
    def scrape(self):
        headers = {'user-agent': random.choice(user_agent_list)}
        if self.Jobtitle:
            response = requests.get(
                f"https://www.104.com.tw/jobs/search/?keyword={self.Jobtitle}&page={self.page}" , headers=headers
            )
   
            Data = BeautifulSoup(response.text , 'lxml')

            jobs_info = Data.find_all('article' , class_ = 'js-job-item')

        company_list = []
        href_list = []
        for job in jobs_info:
            # print(job.find('a',class_="js-job-link").text)
            company = job.get('data-cust-name')
            href = job.find('a').get('href').replace("//" ,"")
            company_list.append(company)
            href_list.append(href)
            # company_list = company_list[2:]
            # href_list = href_list[2:]

        job_href = {company: href for company, href in zip(company_list, href_list)}
        job_href = dict(list(job_href.items())[2:]) ## remove the first two element cause the first two generally are the commercial company
        job_href = {key: 'https://' + value for key, value in job_href.items()}
        # print(job_href)
        # job_href = job_href
        return job_href
        
    def job_detail(self , href):
        ##need to use selenuim to get the data
        ## pending due to the hrome version problem
        all_tool = []
        for company , url in href.items():
            # print(url)
            response = requests.get(
                url
            )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                tools_elements = soup.find_all('a', class_='tools')
                tools_list = [element.get_text(strip=True) for element in tools_elements]
                if tools_list:
                    all_tool.append(tools_list)
        return all_tool



    

if __name__ == "__main__":
    job = JobQuery("Backend" ,"1")
    job_url = job.scrape()
    toolList = job.job_detail(job_url)
    print(toolList)
