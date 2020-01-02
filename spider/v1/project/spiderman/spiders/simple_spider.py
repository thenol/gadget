import requests
import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random 
import scrapy
from urllib.parse import urlencode
import json


class MySpider(scrapy.Spider):
    name='simple'
    start_urls=['http://www.researchgate.net/login']
    allowed_domains = ["researchgate.net"]
    config={
            'login':'zzp18@mails.tsinghua.edu.cn',
            'password':'abcdefg0',
            'cookie_file':'./cookie.txt',
            'url':'http://www.researchgate.net',
            'logfile':'./log.html',
            'keyword':'tsinghua',
            'mem_url':'https://www.researchgate.net/publicinstitutions.FacilityMembershipList.html?institutionKey={name}&page={page}',
            'profile_url':'https://www.researchgate.net/profile.ProfileFeaturedResearchItems.html?accountId=AC%3A5801742',
        }
    def __init__(self, dic):
        self.config['keyword']=dic['keywords']
        self.client_socket=dic['client_socket']
        self.response_head=dic['response_heads']
        self.response_body=dic['response_body']
        
    def save_cookie(self, cookie):
        with open(self.config['cookie_file'],'wb') as f:
            pickle.dump(cookie,f)
        
    def load_cookie(self):
        try:
            with open(self.config['cookie_file'],'rb') as f:
                cookie = pickle.load(f)
            return cookie
        except:
            return False
            
    
    def save_log(self,log):
        with open(self.config['logfile'],'w',encoding='utf-8') as f:
            f.write(log)


    def login(self, token, cookie):
        url=self.start_urls[0]
        data= {
            "request_token":token,
            "login":"zzp18@mails.tsinghua.edu.cn",
            "password":"abcdefg0",
            'urlAfterLogin':'',
            'headerLogin':'yes',
            'setLoginCookie': 'yes',
            'invalidPasswordCount':0,
        }
        response = requests.post(url,data=data,cookies=cookie)
        print('The login status is:{0}\n\n'.format(response.status_code))
        # cookie_tmp=response.cookies
        # self.cookie=cookie_tmp.get_dict()
        if int(response.status_code)==200:
            # print('login successfully, cookie is{0} {1}\n\n'.format(str(cookie_tmp),self.cookie))
            print('login successfully!\n\n')
            return True
        else:
            print('login failed!\n\n')
            return False

    def get_token_cookie(self):
        '''
        处理登录后页面的html
        :param html:
        :return: 获取csrftoken
        '''
        url=self.start_urls[0]
        response=requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        res = soup.find("meta",attrs={"name":"Rg-Request-Token"})
        token = res["content"]
        cookie = response.cookies.get_dict()
        print('the login token is: {0}\n\n'.format(token))

        return token,cookie

    def get_token(self, url, cookie):
        response=requests.get(url, cookies=cookie)
        soup = BeautifulSoup(response.text,'lxml')
        res = soup.find("meta",attrs={"name":"Rg-Request-Token"})
        return res['content']

    def parse(self, resp):
        login_cookie=self.load_cookie()
        if not login_cookie:
            print('re-login for cookie\n\n')
            token, cookie=self.get_token_cookie()
            self.login(token,cookie)
            print('re-gain cookie is:{0}\n\n'.format(cookie))
            self.save_cookie(cookie)#保存登录后cookie，用于后续的操作
        else:
            print('already got cookie:{0}\n\n'.format(login_cookie))
            print('start getting token....\n\n')
            token=self.get_token(self.config['url'], cookie=login_cookie)
            print('got token:{0}\n\n'.format(token))

        # 网页加载
        refer_params={}
        refer_params['query']=self.config['keyword']    
        refer_params['type']='researcher'
        refer_url='https://www.researchgate.net/search.Search.html?'+str(urlencode(refer_params))

        #异步加载
        params={}
        params['query']=self.config['keyword']
        params['activeTab']='institution'
        params['offset']=0
        params['limit']=1000 #默认最多抓取1000个老师
        target_url='https://www.researchgate.net/search.SearchBox.loadMore.html?'+str(urlencode(params))
        header={
            # 'Rg-Request-Token':token,
            # 'Referer':refer_url,
            # 'Accept': 'application/json',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'authority':self.config['url'],
            'method':'GET',
            'path':'/search.SearchBox.loadMore.html?'+str(urlencode(params)),
            'scheme':'https',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests':'1',
            # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
        
        response = requests.get(target_url,cookies=login_cookie, headers=header)#response type :json
        self.save_log(response.text)
        obj=json.loads(response.text)
        institution=obj['result']['state']['searchSearch']['institution']
        institution_items=institution['items']
        print('catched institutions amount:{0}'.format(institution['totalItems']))
        
        for it in institution_items:
            university_name='_'.join(it['displayName'].split(' '))
            print('university: catch the university:{0}\n\n'.format(university_name))
            yield scrapy.Request(self.config['mem_url'].format(name=university_name,page=1),meta={'name':university_name,'header':header},callback=self.parseInstitution,headers=header)#response type :json


    def parseInstitution(self,response):
        '''
            parse the member list from page 0
            data structure:
                peopleListItems:
                    people:

        '''
        result=json.loads(response.text)
        page_amount=result['result']['data']['pager']['totalItems']//25 #分页数量为每页25
        for i in range(0,page_amount+1):
            print('page:    {0}'.format(i))
            yield scrapy.Request(self.config['mem_url'].format(name=response.meta['name'],page=i),callback=self.parseMembers\
                ,headers=response.meta['header'])#response type :json
        

    def parseMembers(self,response):
        '''
            parse people from the list of each page
        '''
        result=json.loads(response.text)
        peopleListItems=result['result']['data']['peopleListItems']
        for o in peopleListItems:
            print('people:  start catching {0}\n\n'.format(o))
            yield scrapy.Request(self.config['mem_url'].format(name=response.meta['name'],page=i),callback=self.parse_profile\
                ,headers=response.meta['header'])#response type :json


    def parse_profile(self,response):
        result=json.loads(response.text)
