from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
from time import sleep, time
import numpy as np
from random import randint
year = [str(i) for i in range(1990, 2018)]
pages = [str(i) for i in range(1, 50)]
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
print('Variables Initialisted')
def flat(a , b):
    for i in a:
        if(type(i) is list):
            flat(i ,b)
        else:
            b.append(i)
print('Web Scraping Started')
for year_url in year:
    print('Scaping year: '+year_url)
    for page in pages:
        print('Scraping year: {} on page: {}'.format(year_url, page))
        url = 'http://www.imdb.com/search/title?release_date='+year_url+'&sort=num_votes,desc&page='+page
        response = get(url)
        if(response.status_code != 200):
            continue
        # sleep(randint(8, 15))
        requests+=1
        elapsed_time = time() - start_time
        print('Requests: {}; , Frequency: {} request/s'.format(requests , requests/elapsed_time))
        soup = bs(response.content ,'html.parser')
        containers = soup.find_all('div', class_ = 'lister-item-content')
        movies = [container for container in containers if(container.find('div', class_='ratings-metascore') is not None)]
        years_.append([movie.find('span' , class_='lister-item-year').text.strip() for movie in movies])
        names_.append([movie.h3.a.text.strip() for movie in movies])
        ratings = [movie.find('div', class_='ratings-bar') for movie in movies]
        imdb_ratings_.append([rating.find('strong').text.strip() for rating in ratings])
        metascores_.append([rating.find('span', class_='metascore').text.strip() for rating in ratings])
        votes_count_.append([votes.find('span' , {'name' :'nv'})['data-value'] for votes in movies])
print('Scraping Complete, flattening started')
flat(names_ , names)
flat(years_, years)
flat(imdb_ratings_, imdb_ratings)
flat(metascores_ , metascores)
flat(votes_count_, votes_count)
print('Flattening Complete, printing Database')
movies_db = pd.DataFrame({
    'Name':names,
    'Year':years,
    'IMDB Rating':imdb_ratings,
    'Metascore':metascores,
    'Number of Votes':votes_count
})
movies_db.to_csv('imdb_db.csv',header=True, columns=['Name','Year','IMDB Rating', 'Metascore','Number of Votes'], index_label =['id'])
