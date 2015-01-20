import json
from kraken.kv.widgets import DraggableWidget


class KrakenJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DraggableWidget): 
            pos = dict(x=obj.x,y=obj.y)
            return dict(in_cv=obj.in_cv, out_cv=obj.out_cv, pos=pos, name=obj.name, id=obj.id, pars=obj.pars)
        return json.JSONEncoder.default(self, obj)