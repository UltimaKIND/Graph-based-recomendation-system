import networkx as nx
import matplotlib.pyplot as plt, mpld3
from graph_recsys.models import Genre, Track, Prefer
from users.models import User


def make_recomentaions(data, user, neighbors, k):
    """
    функция делает рекомендации на основе pagerank когда пользователь еще не выбрал предпочтения
    и не добавил треки в плейлист (узел графа не имеет связей с другими узлами - нельзя определить меру
    схожести с другими узлами) или на основе k-nearest neighbors и коллаборативной фильтрации
    """
    if (
        len(user.track_set.all()) == 0
        and len(Prefer.objects.get(user=user).genres.all()) == 0
    ):
        return get_track(data, user)
    else:
        preferred_genres = Prefer.objects.get(user=user).genres.all()
        user_tracks = user.track_set.all()
        neighbors_tracks = []
        for neighbor in neighbors[:k]:
            neighbors_tracks.extend(list(neighbor[0].track_set.all()))
        all_tracks = [x for x in data["tracks"] if x[0] not in user_tracks]
        preferred_tracks = [
            x
            for x in all_tracks
            if x[0].genre in preferred_genres and x[0] in neighbors_tracks
        ]
        other_tracks = [
            x
            for x in all_tracks
            if x[0].genre not in preferred_genres and x[0] in neighbors_tracks
        ]
        rest = [
            x
            for x in all_tracks
            if x[0] not in preferred_tracks and x[0] not in other_tracks
        ]
        other_tracks.extend(rest)
        preferred_tracks.extend(other_tracks)

        _tracks = [
            x
            for x in data["tracks"]
            if x[0] not in user.track_set.all()
            and x[0].genre in Prefer.objects.get(user=user).genres.all()
        ]
        rec_from_neigbors = [
            x
            for x in data["tracks"]
            if x[0] in neighbors_tracks
            and x[0] not in user.track_set.all()
            and x[0].genre in Prefer.objects.get(user=user).genres.all()
        ]
        additional_data = [x for x in data["tracks"] if x[0] not in rec_from_neigbors]

    return [x[0] for x in preferred_tracks][:5]


def construct_graf(user):
    """
    функция строит граф и возвращает его
    """
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
    return {"graph": G, "source": user_node}


def get_simrank_similarity(data):
    """
    функция возвращает оценку сходства узлов графа
    """
    result = nx.simrank_similarity(data["graph"], data["source"])
    result.pop(data["source"])
    test = [
        (key, value)
        for key, value in result.items()
        if isinstance(key, data["source"].__class__)
    ]
    return sorted(test, key=lambda x: (x[1]), reverse=True)


def get_pagerank(data):
    """
    функция возвращает узлы графа и их pagerank
    """
    ranked_data = nx.pagerank(data["graph"])
    sorted_users = [
        (key.first_name, round(value * 100, 2))
        for key, value in sorted(
            ranked_data.items(), key=lambda item: item[1], reverse=True
        )
        if isinstance(key, User)
    ]
    sorted_tracks = [
        (key, round(value * 100, 2))
        for key, value in sorted(
            ranked_data.items(), key=lambda item: item[1], reverse=True
        )
        if isinstance(key, Track)
    ]
    sorted_genres = [
        (key, round(value * 100, 2))
        for key, value in sorted(
            ranked_data.items(), key=lambda item: item[1], reverse=True
        )
        if isinstance(key, Genre)
    ]
    return {"users": sorted_users, "tracks": sorted_tracks, "genres": sorted_genres}


def draw_graph(graph):
    """
    функция отрисовки графа
    """
    all_users = [x for x in User.objects.all()]
    user_labels = {x: x.first_name for x in User.objects.all()}
    track_labels = {x: x.name for x in Track.objects.all()}
    genre_labels = {x: x.name for x in Genre.objects.all()}
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
    plt.axis("off")
    fig.set_size_inches(15, 15)
    pos = nx.spring_layout(G)
    options = {"edgecolors": "tab:gray", "node_size": 1000, "alpha": 0.9}
    nx.draw_networkx_nodes(
        G, pos, nodelist=(all_users), node_color="tab:red", **options
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=(all_tracks), node_color="tab:green", **options
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=(all_genres), node_color="tab:blue", **options
    )
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, user_labels, font_size=4, font_color="black")
    nx.draw_networkx_labels(G, pos, track_labels, font_size=4, font_color="gray")
    nx.draw_networkx_labels(G, pos, genre_labels, font_size=4, font_color="black")
    g = mpld3.fig_to_html(fig)
    return g


def get_track(data, user):
    """
    функция возвращает топ прослушиваемых треков когда пользователь еще не выбрал предпочтения или треки
    """
    all_tracks = data["tracks"]
    filtered_tracks = [x[0] for x in all_tracks if x[0] not in user.track_set.all()]
    users_prefers = [
        x
        for x in filtered_tracks
        if x.genre in Prefer.objects.get(user=user).genres.all()
    ][:5]
    if len(users_prefers) < 5:
        users_prefers.extend(filtered_tracks[0 : 5 - len(users_prefers)])
    if users_prefers:
        return users_prefers
    return filtered_tracks[:5]
