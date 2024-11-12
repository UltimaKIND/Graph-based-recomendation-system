from tokenize import String
from .nodeutils import NodeUtils
from neomodel import StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, EmailProperty
from django_neomodel import DjangoNode


class UserNode(StructuredNode, NodeUtils):
    user_id = UniqueIdProperty()
    email = EmailProperty()


class TrackNode(StructuredNode, NodeUtils):
    track_id = UniqueIdProperty()
    name = StringProperty()
    artist = StringProperty()
    genre = StringProperty()

class GenreNode(StructuredNode, NodeUtils):
    genre_id = UniqueIdProperty()
    genre = StringProperty()


    # Relations :
    listening = RelationshipTo('TrackNode', 'LISTENED')
    included_in = RelationshipTo('GenreNode','INCLUDED_IN')
    prefers = RelationshipTo('GenreNode', 'PREFER')