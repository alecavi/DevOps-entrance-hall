import requests
from typing import Any, Sequence, List, Dict

from config import VIDEO_INDEX


class Video:
    server: int
    ip: str
    name: str
    file: str
    thumb: str
    pic: str
    uuid: str
    category: str


def _to_video(json: Dict[str, Any]) -> Video:
    video = Video()
    video.server = json["server"]
    video.name = json["name"]
    video.file = json["file"]
    video.thumb = json["thumb"]
    video.pic = json["pic"]
    video.uuid = json["uuid"]
    video.category = json["category"]


def get_random_video() -> Video:
    return _to_video(requests.get(
        VIDEO_INDEX + "/_aggrs/sample-one"
    ).json()[0])


def get_videos_by_uuid(uuids: Sequence[str]) -> List[Video]:
    return list(map(_to_video, requests.get(
        VIDEO_INDEX + '?filter={{"uuid": {{"$in": {} }}'.format(uuids)
    ).json()))
