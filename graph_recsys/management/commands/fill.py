from django.core.management import BaseCommand
from users.models import User
from graph_recsys.models import Genre, Track, Prefer


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        users_for_create = []
        user_list = [
            {'first_name': 'Анастасия', 'email': 'anastasia@mail.ru'},
            {'first_name': 'Станислав', 'email': 'stanislav@internet.ru'},
            {'first_name': 'Александра', 'email': 'alexandra@list.ru'},
            {'first_name': 'Ибрагим', 'email': 'ibragim@mail.ru'},
            {'first_name': 'Аврора', 'email': 'avrora@gmail.com'},
            {'first_name': 'Степан', 'email': 'stepan@bk.ru'},
            {'first_name': 'Виктория', 'email': 'victoria@aol.com'},
            {'first_name': 'Екатерина', 'email': 'ekaterina@bk.ru'},
            {'first_name': 'Глеб', 'email': 'gleb@internet.ru'},
            {'first_name': 'Богдан', 'email': 'bogdan@internet.ru'}
        ]
        for user in user_list:
            user_ = User(**user)
            user_.set_password('123456')
            users_for_create.append(user_)

        User.objects.bulk_create(users_for_create)

        genres_list = [
            {'name': 'Rock'},
            {'name': 'Metall'},
            {'name': 'Electronic'},
            {'name': 'Rap'},
            {'name': 'Pop'}
        ]
        for item in genres_list:
            Genre.objects.create(**item)


        track_list = [
            {'track': {'name': 'Float On', 'artist': 'Modest Mouse', 'genre': Genre.objects.get(name='Rock')}, 'listeners': (3, 6)},
            {'track': {'name': 'Bring Me To Life', 'artist': 'Katherine Jenkins', 'genre': Genre.objects.get(name='Rock')}, 'listeners': (1, 4, 5)},
            {'track': {'name': 'Hey There Delilah', 'artist': 'Plain White T\'s', 'genre': Genre.objects.get(name='Rock')}, 'listeners': (2, 3)},
            {'track': {'name': 'Reverly', 'artist': 'Kings of Leon', 'genre': Genre.objects.get(name='Rock')}, 'listeners': (2, 3, 4)},
            {'track': {'name': 'Heartbreak Warfare', 'artist': 'John Mayer', 'genre': Genre.objects.get(name='Rock')}, 'listeners': (1, 5, 9)},
            {'track': {'name': 'Fade to black', 'artist': 'Metallica', 'genre': Genre.objects.get(name='Metall')}, 'listeners': (1, 4)},
            {'track': {'name': 'The Unforgiven ll', 'artist': 'Metallica', 'genre': Genre.objects.get(name='Metall')}, 'listeners': (1, 4)},
            {'track': {'name': 'Untill it sleeps', 'artist': 'Metallica', 'genre': Genre.objects.get(name='Metall')}, 'listeners': (1, 4)},
            {'track': {'name': 'The Unforgiven lll', 'artist': 'Metallica', 'genre': Genre.objects.get(name='Metall')}, 'listeners': (1, 2)},
            {'track': {'name': 'Alejandro', 'artist': 'Lady Gaga', 'genre': Genre.objects.get(name='Pop')}, 'listeners': (8, 9)},
            {'track': {'name': 'Technologic', 'artist': 'Daft Punk', 'genre': Genre.objects.get(name='Electronic')}, 'listeners': (5, 10)},
            {'track': {'name': 'DVNO', 'artist': 'Justice', 'genre': Genre.objects.get(name='Electronic')}, 'listeners': (5, 6, 8, 10)},
            {'track': {'name': 'Imma Be', 'artist': 'Black Eyed Peas', 'genre': Genre.objects.get(name='Rap')}, 'listeners': (10,)},
            {'track': {'name': 'One Minute to Midnight', 'artist': 'Justice', 'genre': Genre.objects.get(name='Electronic')}, 'listeners': (5, 6, 8, 10)},
            {'track': {'name': 'Fancy Footwork', 'artist': 'Chromeo', 'genre': Genre.objects.get(name='Electronic')}, 'listeners': (6, 7, 8)},
            {'track': {'name': 'Up Up & Away', 'artist': 'Kid Cudi', 'genre': Genre.objects.get(name='Rap')}, 'listeners': (7,)},
            {'track': {'name': 'Never Let You Go', 'artist': 'Third Eye Blind', 'genre': Genre.objects.get(name='Pop')}, 'listeners': (9,)},
            {'track': {'name': 'Hips Don\'t Lie', 'artist':'Shakira', 'genre':Genre.objects.get(name='Pop')}, 'listeners': (9,)},
            {'track': {'name': 'Hailie\'s Song', 'artist': 'Eminem', 'genre': Genre.objects.get(name='Rap')}, 'listeners': (7,)},
            {'track': {'name': 'Waking the Demon', 'artist': 'Bullet for My Valentine', 'genre': Genre.objects.get(name='Metall')}, 'listeners': (2, 3)},
            {'track': {'name': 'It Was A Good Day', 'artist': 'Ice Cube', 'genre': Genre.objects.get(name='Rap')}, 'listeners': (6, 7)},
            {'track': {'name': 'My Name Is', 'artist': 'Eminem', 'genre': Genre.objects.get(name='Rap')}, 'listeners': (6, 7, 9)},
            {'track': {'name': 'U Smile', 'artist': 'Justin Bieber', 'genre': Genre.objects.get(name='Pop')}, 'listeners': (9,)},
            {'track': {'name': 'The Big Gundown', 'artist': 'The Prodigy', 'genre': Genre.objects.get(name='Electronic')}, 'listeners': (3, 10)},
            {'track': {'name': 'Party In The U.S.A', 'artist': 'The Barden Bellas', 'genre': Genre.objects.get(name='Pop')}, 'listeners': ()},
        ]

        for item in track_list:
            track = Track.objects.create(**item['track'])
            track.listeners.add(*item['listeners'])

        prefer_list = [
            {'user': {'user': User.objects.get(id=1),}, 'genres': (1, 2)},
            {'user': {'user': User.objects.get(id=2),}, 'genres': (1, 2)},
            {'user': {'user': User.objects.get(id=3),}, 'genres': (1, 2, 3)},
            {'user': {'user': User.objects.get(id=4),}, 'genres': (1, 2)},
            {'user': {'user': User.objects.get(id=5),}, 'genres': (1, 3)},
            {'user': {'user': User.objects.get(id=6),}, 'genres': (1, 3, 4)},
            {'user': {'user': User.objects.get(id=7),}, 'genres': (3, 4)},
            {'user': {'user': User.objects.get(id=8),}, 'genres': (3, 5,)},
            {'user': {'user': User.objects.get(id=9),}, 'genres': (1, 4, 5)},
            {'user': {'user': User.objects.get(id=10),}, 'genres': (3, 4)},
        ]

        for item in prefer_list:
            prefer = Prefer.objects.create(**item['user'])
            prefer.genres.add(*item['genres'])


