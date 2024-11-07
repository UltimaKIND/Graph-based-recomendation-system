from tokenize import String
from .nodeutils import NodeUtils
from neomodel import StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, EmailProperty
from django_neomodel import DjangoNode


class UserNode(StructuredNode, NodeUtils):
    user_id = UniqueIdProperty()
    email = EmailProperty()

    @property
    def serialize(self):
        return {
            'node_properties': {
                'user_id': self.user_id,
                'email': self.email
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'UserNode',
                'nodes_related': self.serialize_relationships(self.listening.all()),
            },
        ]

class TrackNode(StructuredNode, NodeUtils):
    track_id = UniqueIdProperty()
    name = StringProperty()
    artist = StringProperty()
    genre = StringProperty()


    @property
    def serialize(self):
        return {
            'node_properties': {
                'track_id': self.user_id,
                'name': self.email,
                'artist': self.artist,
                'genre': self.genre,
            },
        }
    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'UserNode',
                'nodes_related': self.serialize_relationships(self.listening.all()),
            },
        ]



class GenreNode(StructuredNode, NodeUtils):
    genre_id = UniqueIdProperty()
    genre = StringProperty()

    @property
    def serialize(self):
        return {
            'node_properties': {
                'genre_id': self.user_id,
                'genre': self.email
            },
        }

    # Relations :
    listening = RelationshipTo('TrackNode', 'LISTENED')
    included_in = RelationshipTo('GenreNode','INCLUDED_IN')
    prefers = RelationshipTo('GenreNode', 'PREFER')