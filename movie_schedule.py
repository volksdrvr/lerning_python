current_movies = {'Animal House': '11:00am',
                  'Squid Game': '1:00pm',
                  'Stargate': '3:00pm',
                  'Blade Runner': '5:00pm'}

print("We are showing the following movies:")
for key in current_movies:
    print(key)
movie = input('What movie would you like the showtime for?\n')

showtime = current_movies.get(movie)
if showtime == None:
    print("The movie showtime isn't playing")
else:
    print(movie, "is playing at", showtime)