from django.db.models import Q, QuerySet
import networkx as nx

import math
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt, mpld3
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
from numpy.ma.core import not_equal

from graph_recsys.models import Genre, Track, Prefer

from users.models import User


def dotProduct(vecA, vecB):
    '''
    функция вычисляющая скалярное произведение векторов
    '''
    d = 0.0
    for dim in vecA:
        if dim in vecB:
            d += vecA[dim] * vecB[dim]
    return d

def distCosine (vecA, vecB):
    '''
    функция вычисляющая косинусное расстояние между двумя векторами
    '''
    d = 0.0
    #for dim in vecA:
    #    if dim in vecB:
    #        d += vecA[dim] * vecB[dim]
    #if d == 0:
    #    return d
    #return d / math.sqrt(d) / math.sqrt(d)
    for dim in vecA:
        if dim in vecB:
            d += vecA[dim] * vecB[dim]
    if d == 0:
        return 0
    return d/math.sqrt(d**2)



def get_data():
    users = User.objects.all() # !!! ZeroDivisionError - у пользователя нет данных
    #users = User.objects.filter(~Q(first_name='Руслан'))

    user_genres_dict = {}
    for user in users:
        all_genres = Genre.objects.all()
        #user_genres = Prefer.objects.filter(user=user).first().genres.all()

        user_tracks = user.track_set.all()
        user_genres_dict[user] = {x.name: len(user_tracks.filter(genre=x)) for x in all_genres}
    return user_genres_dict

def make_recomendation(user, userRates = get_data(), nTopUsers=5, nTopTracks=5):
    #matches = [(u, distCosine(userRates[user], userRates[u])) for u in userRates]
    matches = []
    for u in userRates:
        matches.append((u, distCosine(userRates[user], userRates[u])))
    bestMatches = sorted(matches, key=lambda x: x[1], reverse=True)[:]
    sim = dict()
    sim_all = sum([x[1] for x in bestMatches])
    bestMatches = dict([x for x in bestMatches if x[1]>0.5])
    for relatedUser in bestMatches:
        for genre in userRates[relatedUser]:
            if not genre in userRates[user]:
                if not genre in sim:
                    sim[genre] = 0.0
                sim[genre] += userRates[relatedUser][genre] * bestMatches[relatedUser]
    for product in sim:
        sim[product] /= sim_all
    bestProducts = sorted(sim, key=lambda x: x[1], reverse=True)[:nTopTracks]
    return matches

def make_recomentaions(data, user, neighbors, k):
    if len(user.track_set.all()) == 0 and len(Prefer.objects.get(user=user).genres.all()) == 0:
        return get_track(data, user)
    else:
        preferred_genres = Prefer.objects.get(user=user).genres.all()
        user_tracks = user.track_set.all()
        neighbors_tracks = []
        for neighbor in neighbors[:k]:
            neighbors_tracks.extend(list(neighbor[0].track_set.all()))
        all_tracks = [x for x in data['tracks'] if x[0] not in user_tracks]
        preferred_tracks = [x for x in all_tracks if x[0].genre in preferred_genres and x[0] in neighbors_tracks]
        other_tracks = [x for x in all_tracks if x[0].genre not in preferred_genres and x[0] in neighbors_tracks]
        rest =  [x for x in all_tracks if x[0] not in preferred_tracks and x[0] not in other_tracks]
        other_tracks.extend(rest)
        preferred_tracks.extend(other_tracks)





        _tracks = [x for x in data['tracks'] if x[0] not in user.track_set.all() and x[0].genre in Prefer.objects.get(user=user).genres.all()]
        rec_from_neigbors = [x for x in data['tracks'] if x[0] in neighbors_tracks and x[0] not in user.track_set.all() and x[0].genre in Prefer.objects.get(user=user).genres.all()]
        additional_data = [x for x in data['tracks'] if x[0] not in rec_from_neigbors]

    return [x[0] for x in preferred_tracks][:5]

def construct_graf(user):
    user_node = user
    all_users = User.objects.all()
    all_tracks = Track.objects.all()
    all_genres = Genre.objects.all()

    tracks_users_edges = []
    tracks_genres_edges = []
    for track in Track.objects.all():
        tracks_genres_edges.extend([(track, track.genre)])
        tracks_users_edges.extend([(track, x) for x in track.listeners.all()])

    users_genres_edges = []
    for prefer in Prefer.objects.all():
        users_genres_edges.extend([(prefer.user, x) for x in prefer.genres.all()])

    G = nx.Graph()
    G.add_nodes_from(all_users)
    G.add_nodes_from(all_tracks)
    G.add_nodes_from(all_genres)
    G.add_edges_from(tracks_genres_edges)
    G.add_edges_from(tracks_users_edges)
    G.add_edges_from(users_genres_edges)
    return {'graph': G, 'source': user_node}

def get_knn(data):
    nx.average_neighbor_degree(data['graph'])

def get_neighbors(data):
    return set(data['graph'].neighbors(data['source']))

def get_simrank_similarity(data):
    result = nx.simrank_similarity(data['graph'], data['source'])
    result.pop(data['source'])
    test = [(key, value) for key, value in result.items() if isinstance(key, data['source'].__class__)]
    #return test
    #return max(test, key=test.get)
    return sorted(test, key=lambda x: (x[1]), reverse=True)

def get_pagerank(data):
    ranked_data = nx.pagerank(data['graph'])
    # users = {key: value for key, value in result.items() if isinstance(key, User)}
    sorted_users = [(key.first_name, round(value*100, 2)) for key, value in sorted(ranked_data.items(), key=lambda item: item[1], reverse=True) if isinstance(key, User)]
    #tracks = {key: value for key, value in result.items() if isinstance(key, Track)}
    sorted_tracks = [(key, round(value*100, 2)) for key, value in sorted(ranked_data.items(), key=lambda item: item[1], reverse=True) if isinstance(key, Track)]
    # genres = {key: value for key, value in result.items() if isinstance(key, Genre)}
    sorted_genres = [(key, round(value*100, 2)) for key, value in sorted(ranked_data.items(), key=lambda item: item[1], reverse=True) if isinstance(key, Genre)]


    return {'users': sorted_users, 'tracks': sorted_tracks, 'genres': sorted_genres}

def get_track(data, user):
    all_tracks = data['tracks']
    tracks = [x[0] for x in all_tracks]
    filtered_tracks = [x[0] for x in all_tracks if x[0] not in user.track_set.all()]
    users_prefers = [x for x in filtered_tracks if x.genre in Prefer.objects.get(user=user).genres.all()][:5]
    if len(users_prefers) < 5:
        users_prefers.extend(filtered_tracks[0:5-len(users_prefers)])
    if users_prefers:
        return users_prefers
    return filtered_tracks[:5]

def draw_graph(graph):
    all_users = [x for x in User.objects.all()]
    user_labels = {x:x.first_name for x in User.objects.all()}
    track_labels = {x:x.name for x in Track.objects.all()}
    genre_labels = {x:x.name for x in Genre.objects.all()}
    all_tracks = [x for x in Track.objects.all()]
    all_genres = [x for x in Genre.objects.all()]
    tracks_genres_edges = []
    for track in Track.objects.all():
        tracks_genres_edges.extend([(track, track.genre)])
    user_genres_edges = []
    for prefer in Prefer.objects.all():
        user_genres_edges.extend([(prefer.user, x) for x in prefer.genres.all()])
    user_track_edges = []
    for user in User.objects.all():
        user_track_edges.extend([(user, x) for x in user.track_set.all()])

    G = nx.Graph()
    G.add_nodes_from(all_users)
    G.add_nodes_from(all_tracks)
    G.add_nodes_from(all_genres)
    G.add_edges_from(tracks_genres_edges)
    G.add_edges_from(user_genres_edges)
    G.add_edges_from(user_track_edges)

    fig, ax = plt.subplots()
    ax.grid(False)
    fig.set_size_inches(15, 15)
    pos = nx.spring_layout(G)
    options = {"edgecolors": "tab:gray", "node_size": 1000, "alpha": 0.9}
    nx.draw_networkx_nodes(G, pos, nodelist=(all_users), node_color="tab:red", **options)
    nx.draw_networkx_nodes(G, pos, nodelist=(all_tracks), node_color="tab:green", **options)
    nx.draw_networkx_nodes(G, pos, nodelist=(all_genres), node_color="tab:blue", **options)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, user_labels, font_size=4, font_color="black")
    nx.draw_networkx_labels(G, pos, track_labels, font_size=4, font_color="gray")
    nx.draw_networkx_labels(G, pos, genre_labels, font_size=4, font_color="black")
    g = mpld3.fig_to_html(fig)
    return g




