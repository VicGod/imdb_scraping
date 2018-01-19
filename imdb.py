from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
from time import sleep, time
import numpy as np
from random import randint
from multiprocessing import Pool
year = [str(i) for i in range(1990, 2018)]
pages = [str(i) for i in range(1, 40)]
start_time = time()
names =[]
names_ = []
years = []
years_ = []
metascores = []
metascores_ = []
imdb_ratings = []
imdb_ratings_ = []
votes_count = []
votes_count_ = []
requests = 0
headers = {"Accept-Language": "en-US, en;q=0.5"}
print('Variables Initialisted')
def flat(a , b):
    for i in a:
        if(type(i) is list):
            flat(i ,b)
        else:
            b.append(i)

def parse(year_url_ , page_):
    global requests,names_,years_,votes_count_,imdb_ratings_,metascores_
    print('Scraping year: {} on page: {}'.format(year_url_, page_))
    url = 'http://www.imdb.com/search/title?release_date='+year_url_+'&sort=num_votes,desc&page='+page_
    response = get(url, headers=headers)
    if(response.status_code != 200):
        return
    # sleep(randint(8, 15))
    # requests+=1
    # elapsed_time = time() - start_time
    # print('Requests: {}; , Frequency: {} request/s'.format(requests , requests/elapsed_time))
    soup = bs(response.content ,'html.parser')
    containers = soup.find_all('div', class_ = 'lister-item-content')
    movies = [container for container in containers if(container.find('div', class_='ratings-metascore') is not None)]
    years_.append([movie.find('span' , class_='lister-item-year').text.strip() for movie in movies])
    names_.append([movie.h3.a.text.strip() for movie in movies])
    ratings = [movie.find('div', class_='ratings-bar') for movie in movies]
    imdb_ratings_.append([rating.find('strong').text.strip() for rating in ratings])
    metascores_.append([rating.find('span', class_='metascore').text.strip() for rating in ratings])
    votes_count_.append([votes.find('span' , {'name' :'nv'})['data-value'] for votes in movies])

# if __name__=='__main__':
print('Web Scraping Started')
for year_url in year:
    print('Scraping year: '+year_url)
    for page in pages:
        parse(year_url, page)
        # p = Pool(processes=2)
        # p.apply_async(parse, (year_url,page,))
        # p.terminate()


print('Scraping Complete, flattening started')
flat(names_ , names)
flat(years_, years)
flat(imdb_ratings_, imdb_ratings)
flat(metascores_ , metascores)
flat(votes_count_, votes_count)
print('Flattening Complete, printing Database')
years = [int(rating[-5:-1]) for rating in years]
imdb_ratings = [float(rating) for rating in imdb_ratings]
metascores = [int(rating) for rating in metascores]
votes_count = [int(rating) for rating in votes_count]

movies_db = pd.DataFrame({
    'Name':names,
    'Year':years,
    'IMDB Rating':imdb_ratings,
    'Metascore':metascores,
    'Number of Votes':votes_count
})
movies_db.to_csv('imdb_db.csv',header=True, columns=['Name','Year','IMDB Rating', 'Metascore','Number of Votes'], index_label =['id'], encoding='utf-8')
