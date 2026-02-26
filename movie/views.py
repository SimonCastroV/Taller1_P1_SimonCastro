from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import base64, urllib
# Create your views here.

def home(request):
    #return HttpResponse("Welcome to home page")
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Simon Castro Valencia'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse("Welcome to about page")
    return render (request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render (request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')  
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if years:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
        
    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))
    
    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    
        # =========================
    # GRÁFICA: PELÍCULAS POR GÉNERO
    # (SOLO PRIMER GÉNERO)
    # =========================
    genres = Movie.objects.values_list('genre', flat=True)
    genre_counts = {}

    for genre in genres:
        if genre:
            first_genre = genre.split(',')[0].strip()
        else:
            first_genre = 'Unknown'

        if first_genre in genre_counts:
            genre_counts[first_genre] += 1
        else:
            genre_counts[first_genre] = 1

    plt.figure(figsize=(10, 5))
    plt.bar(genre_counts.keys(), genre_counts.values())
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.4)

    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()

    graphic_genre = base64.b64encode(buffer_genre.getvalue()).decode('utf-8')
    buffer_genre.close()


    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic_genre': graphic_genre
    })