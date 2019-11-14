import json
from invalid_tags import invalid_tags
from venues.manage_venue import search_venue
from area_list import map_query_to_venue


def set_area_name(tag):
    area_name = map_query_to_venue(tag)
    if area_name is None: 
        return None
    return area_name
        
def set_venue_name(area, hashtags):
    for hashtag in hashtags:
        if hashtag not in invalid_tags:
            if search_venue(area, hashtag):
                return hashtag
    return None    


def start_filter(data, tag):
    data_list = []
    data_list = json.loads(data)
    idx_to_del = []

    for i in range(len(data_list)):
        post = data_list[i]
        post["area_name"] = set_area_name(tag)
        venue = set_venue_name(post["area_name"], post["hashtags"])
        if venue == None:
            idx_to_del.append(i)
        else:
            post["venue_name"] = venue

    shift = 0
    for idx in idx_to_del:
        del data_list[idx-shift]
        shift += 1

    return json.dumps(data_list)
