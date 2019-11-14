from invalid_tags import invalid_tags
from list_restaurant.list_manager import read_venue_list

dict_post = {"key": "https://www.instagram.com/p/B4prB3AlUsL/", 
"datetime": "2019-11-09T16:19:10.000Z", 
"img_urls": ["https://scontent-icn1-1.cdninstagram.com/vp/ad505d075620635c526d5bf754b06a72/5E483CC1/t51.2885-15/e35/s1080x1080/73414170_145149603460189_4099047723666018059_n.jpg?_nc_ht=scontent-icn1-1.cdninstagram.com&_nc_cat=101", "https://scontent-icn1-1.cdninstagram.com/vp/ff3019d4ea2a3f2c671ae08811d5f6ea/5E50E4FC/t51.2885-15/e35/s1080x1080/71139621_452764652033226_8805805296712880998_n.jpg?_nc_ht=scontent-icn1-1.cdninstagram.com&_nc_cat=106", "https://scontent-icn1-1.cdninstagram.com/vp/065567409d1d53a786efc5a50b59a13f/5E5ECC59/t51.2885-15/e35/s1080x1080/73533224_416113905731575_4222982922381580875_n.jpg?_nc_ht=scontent-icn1-1.cdninstagram.com&_nc_cat=107", "https://scontent-icn1-1.cdninstagram.com/vp/9413968250b9af61fd8a358445a7fea9/5E4D1971/t51.2885-15/e35/s1080x1080/71727263_155899355630292_3331786797527077413_n.jpg?_nc_ht=scontent-icn1-1.cdninstagram.com&_nc_cat=100", "https://scontent-icn1-1.cdninstagram.com/vp/d40e8cffcc5de87cc2aba2cf25742c93/5E5163FE/t51.2885-15/e35/s1080x1080/72711488_408580983351465_9388894737222604_n.jpg?_nc_ht=scontent-icn1-1.cdninstagram.com&_nc_cat=109", "https://scontent-icn1-1.cdninstagram.com/vp/5fffa8e6007dc0c6d650f0cc46b102f7/5E62DB79/t51.2885-15/e35/s1080x1080/70477530_461613821130637_5120640483431293929_n.jpg?_nc_ht=scontent-icn1-1.cdninstagram.com&_nc_cat=101", "https://scontent-icn1-1.cdninstagram.com/vp/89521340f6d0c844491ba5c5310d9e4a/5E54E075/t51.2885-15/e35/s1080x1080/72329392_773000013142329_4337433399358311329_n.jpg?_nc_ht=scontent-icn1-1.cdninstagram.com&_nc_cat=109"], 
"hashtags": ["2차🍷", "오카찬스", "호호세세", "성수호호세세", "성수맛집", "서울숲맛집", "성수핫플", "서울숲핫플"]}

invalid_tags = ["성수맛집", "성수핫플", "서울숲핫플", "서울숲커피", "서울숲맛집", "서울숲맛집", "서울숲카페", "서울숲", "cafe", "coffe", "인테리어", "사진맛집", "맛집"]

for tag in dict_post["hashtags"]:
    if tag not in invalid_tags:
        if tag in read_venue_list("./list_restaurant/seongdonggu.json", "seongdonggu"):
            return tag
return -1