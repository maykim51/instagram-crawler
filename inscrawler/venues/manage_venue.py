import json
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['scc-hotplace']
collection = db['venues']


area_list = [
        "가로수길", 
        "강남역",
        "건대",
        "경리단길",
        "광화문",
        "남양주",
        "대학로",
        "망원",
        "명동",
        "문래",
        "북촌",
        "분당",
        "상수",
        "샤로수길",
        "서래마을",
        "서촌",
        "성수",
        "송도",
        "압구정",
        "양재",
        "양평",
        "여의도",
        "연남",
        "을지로",
        "이태원",
        "익선동",
        "인사동",
        "일산",
        "잠실",
        "종로",
        "청담동",
        "한남동",
        "합정",
        "해방촌",
        "홍대"
]

def update_venue_list(file, area):
    if area not in area_list:
        print(area + ": No such area. Could not insert the file into db.")
        return
        
    with open(file, 'r',  encoding="utf8") as f:
        data = json.loads(f.read())
        data = data["DATA"]
        venue_list = []
        for item in data:
            item = item["upso_nm"].replace(" ", "")
            venue_list.append(item)
        venue_list = list(set(venue_list))
        for venue in venue_list:
            collection.insert_one({"area_name": area, "venue_name": venue})


def search_venue(area_name, venue_name):
    data = {}
    data = collection.find({"area_name": area_name, "venue_name": venue_name}).limit(1)
    if data.count() == 0:
        return None
    else:
        for doc in data:
            return doc

def read_venue_list(file, area):   
    with open(file, 'r',  encoding="utf8") as f:
        data = json.loads(f.read())
        if area in data.keys():
            return data[area]
        else:
            print("no such area")
            return -1     
        
if __name__ == "__main__":
    ### updated lists
    # update_venue_list("gangnamgu.json", "강남역")
    # update_venue_list("seochogu.json", "강남역")
    # update_venue_list("seongdonggu.json", "성수")

    search_venue("강남역", "티엔티엔티엔")
    