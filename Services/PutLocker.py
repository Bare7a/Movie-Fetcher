import re
import json
import requests
from pyquery import PyQuery as pq

from Services.Models.Movie import Movie 
from Services.Models.Server import Server
from Services.Models.Service import Service

DOMAIN = 'https://www9.putlocker.vip'
SEARCH_API = DOMAIN + '/movie/search/'
MOVIE_EMBED_API = DOMAIN + '/ajax/movie_embed/'
MOVIE_EPISODES_API = DOMAIN + '/ajax/movie_episodes/'

class PutLocker(Service):
    def getAllMovieTitles(self, movieName):
        searchUrl = SEARCH_API + movieName
        session = requests.Session()
        response = session.get(searchUrl, headers={'User-Agent': 'Mozilla/5.0'})

        html = response.text
        d = pq(html)
        mlItems = d('.ml-item')
        mlItemsCount = mlItems.size()

        self.movies = []
        for i in range(mlItemsCount):
            mlItem = mlItems.eq(i)
            mlLink = mlItem('a')

            mId = re.findall('[0-9]+', mlLink.attr['data-url'])[0]
            mUrl = MOVIE_EPISODES_API + mId
            mTitle = mlLink.attr['title']

            movie = Movie(mId, mUrl, mTitle, i + 1)
            self.movies.append(movie)

        return self.movies      

    def getAllAvailableLinks(self, urlAddress):
        d = pq(url=urlAddress).html()
        iRe = 'id="\\\\&quot;ep-(.*?)\\\\&quot;"'
        tRe = '<strong>(Server.*?)\\\\n'
        qRe = 'title="\\\\&quot;(.*?)\\\\&quot;"'

        seIds = re.findall(iRe, d)
        seTitles = re.findall(tRe, d)
        seQualities = re.findall(qRe, d)

        seIdsCount = len(seIds)
        seTitlesCount = len(seTitles)
        seQualitiesCount = len(seQualities)

        if not(seIdsCount == seTitlesCount == seQualitiesCount):
            raise Exception('ERROR IN GETTING SERVER IDS')

        self.servers = []
        for i in range(seIdsCount):
            sId = seIds[i]
            sUrl = json.loads(pq(MOVIE_EMBED_API + sId).html())['src']
            sTitle = '[{quality}] {title}'.format(title=seTitles[i], quality=seQualities[i])

            server = Server(sId, sUrl, sTitle)
            self.servers.append(server)

        return self.servers

    def getAllAvailableLinksById(self, movieId):
        moviesCount = len(self.movies)
        if(movieId >= 0 and movieId < moviesCount):
            movieUrl = self.movies[movieId].url
            self.servers = self.getAllAvailableLinks(movieUrl)
            return self.servers
        else:
            raise Exception('ID OF MOVIE OUT OF RANGE')
