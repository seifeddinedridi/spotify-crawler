from dataclasses import dataclass
from typing import List, Optional

from yaml import YAMLObject, Loader, Dumper


@dataclass
class Album(YAMLObject):
    name: str
    release_date: str
    total_tracks: int
    spotify_url: str

@dataclass
class Artist(YAMLObject):
    name: str
    spotify_handle: str
    profile_photo_url: Optional[str]
    genres: List[str]
    popularity: int
    followers: int
    spotify_url: str
    albums: List[Album]
    singles: List[Album]
    yaml_loader = Loader
    yaml_dumper = Dumper