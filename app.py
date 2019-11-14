from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from area_list import map_query_to_venue
from area_list import validate_area_name
import json

app = Flask(__name__)
api = Api(app)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['scc-hotplace']


@app.route('/')
def home():
    return {"message": "Hi this is home!"}
#    return render_template('index.html')

'''
/api/v1/venueList?area_name=홍대
/api/v1/venues?store_name=족발이기가막혀
'''

#error_handling
def abort_if_area_doesnt_exist(area_name):
    # FIXIT find the right area name for the given query
    area = map_query_to_venue(area_name)
    if area == None:
        abort(404, message = "Cannot find area with the given query {}.".format(area_name))
    else:
        return area

# @app.route('/areas/<string:area_name>')
# def get(area_name):
#         area = abort_if_area_doesnt_exist(area_name)
#         # FIXIT search for right times
#         data = db.areas.find({"area_name": "성수"},{"_id":0, "area_name":0})
#         return jsonify({'result':'success', 'venues':list(data)}), 200

class Area(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "area_name", 
        required=True,
        help="Please give area_name."
    )

    def get(self, area_name):
        area = abort_if_area_doesnt_exist(area_name)
        # FIXIT search for right times
        data = list(db.areas.find({"area_name": "성수"},{"_id":0, "area_name":0}))
        print(Data)
        return {'result':'success', 'venues':'sample'}

    
    # def put(self, area_name):
    #     if validate_area_name is False:
    #         return {"message": "Invalid area name."}
    #     start_crawler(area_name)
    #     return {"message": "Succesfully updated!"}
        

        
    # def get_maplist(self):
    #     print('called map list.')
    #     return {'message': 'called the map list.'}
    
    # def put(self, mapId):
    #     '''
    #     ADD validity check
    #     '''
    #     #if not valid:
    #     #   return 400, {"message" : "The map data is invalid."}
        
    #     # data = request.get_json()
    #     data = Map.parser.parse_args()
    #     maps[mapId] = data      
        
    #     db.maps.insert_one({mapId: data})
    #     return {'mapId': mapId, 'map': maps[mapId], 'status': 200}

class Venue(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "venue_name", 
        required=True,
        help="Please give a venue_name."
    )

    def get(self, area_name, venue_name):
        area = abort_if_area_doesnt_exist(area_name)
        venue_name = abort_if_area_doesnt_exist(venue_name)
        venue = db.venues.find({},{'_id':0})
        # FIXIT attach db here
        res = {"venue_name": venue_name, "area": area}
        return res, 200

# @app.route('/post', methods=['GET'])
# def view():
#    posts = db.articles.find({},{'_id':0})
#    return jsonify({'result':'success', 'articles':list(posts)})

api.add_resource(Area, '/areas/<string:area_name>')
api.add_resource(Venue, '/venues/<string:area_name>/<string:venue_name>')


# @app.route('/post', methods=['POST'])
# def post():
#    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
#    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

#    article = {'url': url_receive, 'comment': comment_receive, 'image': url_image, 'title': url_title, 'desc': url_description}

#    db.articles.insert_one(article)

#    return jsonify({'result': 'success'})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)