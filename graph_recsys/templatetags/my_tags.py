from django import template
from graph_recsys.models import Prefer, Track

register = template.Library()

# фильтры для текущего пользователя
@register.filter()
def get_user_prefers(user):
    return ', '.join([x.name for x in Prefer.objects.get(user=user).genres.all()])

@register.filter()
def get_user_tracks(user):
    return ', '.join([x.name for x in user.track_set.all()])

# фильтры для остальных пользователей
@register.filter()
def get_object(data):
    return data[0]

@register.filter()
def get_object_email(data):
    return data[0].email

@register.filter()
def get_object_prefers(data):
    return ', '.join([x.name for x in Prefer.objects.get(user=data[0]).genres.all()])

@register.filter()
def get_object_tracks(data):
    return ', '.join([x.name for x in data[0].track_set.all()])

@register.filter()
def get_value(data):
    return round(data[1], 2)

# фильтры для треков
@register.filter()
def get_track_name(data):
    return data[0].name

@register.filter()
def get_track_artist(data):
    return data[0].artist

@register.filter()
def get_track_genre(data):
    return data[0].genre

@register.filter()
def get_track_value(data):
    return round(data[1], 2)

# фильтры для жанров
@register.filter()
def get_genre_fans(data):
    return len(Prefer.objects.filter(genres=data[0]))

@register.filter()
def get_genre_tracks(data):
    return ', '.join([x.name for x in Track.objects.filter(genre=data[0])])

@register.filter()
def get_genre_value(data):
    return round(data[1], 2)

