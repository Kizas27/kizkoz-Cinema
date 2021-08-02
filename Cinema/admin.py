from django.contrib import admin

from .models import Movie, Genre, Sessions, Tickets, Seats


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'genre',
                    'rating',
                    'duration',
                    'date',
                    'image',
                    'description'
                    )


class SessionAdmin(admin.ModelAdmin):
    list_display = ('date',
                    'movie',
                    )


class TicketsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sold',
        'session',
        'price'
    )


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Sessions, SessionAdmin)
admin.site.register(Seats)
admin.site.register(Tickets, TicketsAdmin)
