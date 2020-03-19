from Services.PutLocker import PutLocker

def main():
    services = []
    services.append(PutLocker())
    # services.append(PutLocker())

    fetchMovieTitles(services)
    service = selectService(services)
    movieId = selectMovieId(service)
    servers = service.getAllAvailableLinksById(movieId)
    showAvailableServers(servers)

def fetchMovieTitles(services):
    movieName = False
    hasMovies = False
    while(not(movieName) or not(hasMovies)):
        movieName = input('Movie Name: ')
        if(movieName):
            for service in services:
                service.getAllMovieTitles(movieName)
                if(service.movies):
                    hasMovies = True
            if(not(hasMovies)):
                print('No movies were found for: {movieName}'.format(movieName=movieName))
        else:
            print('Please write the title of the movie')
    print()

def selectService(services):
    serviceId = False
    servicesCount = len(services)
    print('--- Select a Service ---')
    while(not(serviceId)):
        for i in range(servicesCount):
            print()
            service = services[i]
            print('[{id}] {serviceName}'.format(id=i + 1, serviceName=type(service).__name__ ))
            for movie in service.movies:
                print('--- {movieTitle}'.format(movieTitle=movie.title))
        print()
        serviceId = input('Service Number [1 - {servicesCount}]: '.format(servicesCount=servicesCount))
        try:
            serviceId = int(serviceId)
            if(serviceId > servicesCount or serviceId < 1):
                serviceId = False
        except:
            serviceId = False
        print()
    serviceId = serviceId - 1
    service = services[serviceId]
    return service

def selectMovieId(service):
    movieId = False
    moviesCount = len(service.movies)
    while(not(movieId)):
        print('--- Select a Movie ---')
        for movie in service.movies:
            print(movie)
        
        print()
        movieId = input('Movie Number [1 - {moviesCount}]: '.format(moviesCount=moviesCount))
        try:
            movieId = int(movieId)
            if(movieId > moviesCount or movieId < 1):
                movieId = False
        except:
            movieId = False
        print()
    movieId = movieId - 1
    return movieId

def showAvailableServers(servers):
    print('Available Links: ')
    print()
    for server in servers:
        print(server)

main()
