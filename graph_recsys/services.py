import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt, mpld3

from graph_recsys.models import Genre, Track, Prefer

from users.models import User


def get_recomendation(user):
    G = nx.Graph()
    all_users = [(x.id, {'email': x.__str__()}) for x in User.objects.all()]
    tracks_offset = len(all_users)
    all_tracks = [(x.id+tracks_offset, {'name': x.__str__()}) for x in Track.objects.all()]
    user_tracks_edges = []
    for track in Track.objects.all():
        user_tracks_edges.extend([(track.id+tracks_offset, x.id) for x in track.listeners.all()])

    genres_offset = tracks_offset + len(all_tracks)
    all_genres = [(x.id+genres_offset, {'name': x.__str__()}) for x in Genre.objects.all()]

    user_genres_edges = []
    for prefer in Prefer.objects.all():
        user_genres_edges.extend([(prefer.user_id, x.id+genres_offset) for x in prefer.genres.all()])
    G.add_nodes_from(all_users)
    G.add_nodes_from(all_tracks)
    G.add_nodes_from(all_genres)
    G.add_edges_from(user_tracks_edges)
    G.add_edges_from(user_genres_edges)


    fig, ax = plt.subplots()

    nx.draw(G, with_labels=True)
    g = mpld3.fig_to_html(fig)

    return g


