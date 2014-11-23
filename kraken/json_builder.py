import json
from widgets import DraggableWidget


class KrakenJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DraggableWidget): 
            pos = dict(x=obj.x,y=obj.y)
            return dict(in_cv=[], out_cv=[], pos=pos, name=obj.name, id=obj.id)
        return json.JSONEncoder.default(self, obj)