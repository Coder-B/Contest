#coding=utf-8
import re
import json
import os
import oss2
import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkobjectdet.request.v20191230.DetectVehicleRequest import DetectVehicleRequest
from aliyunsdkocr.request.v20191230.RecognizeCharacterRequest import RecognizeCharacterRequest
from aliyunsdkobjectdet.request.v20191230.RecognizeVehiclePartsRequest import RecognizeVehiclePartsRequest
from PIL import Image


accessKeyId = ''
accessSecret = ''
ossbucketname = ''
def uploadImg(localImgPath):
    auth = oss2.Auth(accessKeyId, accessSecret)
    bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', ossbucketname)
    objectName = os.path.split(localImgPath)[-1]
    resp = bucket.put_object_from_file(objectName, localImgPath)
    if hasattr(resp,"status") and 200 == resp.status :
        return "http://"+ossbucketname+".oss-cn-shanghai.aliyuncs.com/"+objectName
    else:
        return None

def isNoiseCar(item, minWidth, minHeight):
    width = item["Boxes"][2]-item["Boxes"][0]
    height = item["Boxes"][3]-item["Boxes"][1]
    print("width: ", width, ", height: ",height, "minWidth: ", minWidth, ", minHeight: ",minHeight)
    return width < minWidth or height < minHeight

def extractNormalWords(text):
    words = re.findall("[A-Za-z0-9]+", text)
    return ''.join(words)

def isParkingLotsText(text):
    if len(text)>=6:
        return False
    else:
        matchRet = re.search(r"[A-Za-z\s\-]*[0-9]+[A-Za-z]*",text)
        return matchRet is not None and text == matchRet.string

def getCharBoxCenter(charBox):
    rect = charBox["TextRectangles"]
    return [float(rect["Left"])+float(rect["Width"])/2, float(rect["Top"])+float(rect["Height"])/2]

def recognizeCharacter(imgUrl):
    client = AcsClient(accessKeyId, accessSecret, 'cn-shanghai')
    request = RecognizeCharacterRequest()
    request.set_accept_format('json')
    request.set_ImageURL(imgUrl)
    request.set_MinHeight(10)
    request.set_OutputProbability(True)
    response = client.do_action_with_exception(request)
    respStr = str(response, encoding='utf-8')
    # respStr = '{"Data":{"Results":[{"Text":"S*MC 197","Probability":"0.447662353515625","TextRectangles":{"Top":"579.2178955078125","Angle":"-89.835968017578125","Height":"104.97098541259766","Width":"23.869152069091797","Left":"792.7357177734375"}},{"Text":"B124","Probability":"0.79086029529571533","TextRectangles":{"Top":"651.5474853515625","Angle":"-0.098757326602935791","Height":"24.435932159423828","Width":"214.93746948242188","Left":"1225.8492431640625"}},{"Text":"B125","Probability":"0.45939517021179199","TextRectangles":{"Top":"660.3438720703125","Angle":"-0.22820673882961273","Height":"27.854558944702148","Width":"195.37454223632812","Left":"724.8609619140625"}},{"Text":"B126","Probability":"0.50002765655517578","TextRectangles":{"Top":"568.66717529296875","Angle":-89.4033203125,"Height":"214.72618103027344","Width":"29.135915756225586","Left":"244.80532836914062"}}]},"RequestId":"AA3E4A8C-2B96-4A6C-988E-2449C5FB44BA"}'
    # respStr = '{"Data":{"Results":[{"Text":"B124","Probability":"0.88726329803466797","TextRectangles":{"Top":"929.829833984375","Angle":"-89.677406311035156","Height":"350.43377685546875","Width":"40.770416259765625","Left":"2182.83642578125"}},{"Text":"B125","Probability":"0.32054206728935242","TextRectangles":{"Top":"1096.3551025390625","Angle":"-0.11144198477268219","Height":"48.667243957519531","Width":321.47607421875,"Left":"1196.5035400390625"}},{"Text":"8126","Probability":"0.50016641616821289","TextRectangles":{"Top":950.69775390625,"Angle":"-89.064460754394531","Height":"350.64254760742188","Width":"46.894298553466797","Left":"405.09701538085938"}},{"Text":"tttt","Probability":"0.94583821296691895","TextRectangles":{"Top":"1347.6053466796875","Angle":"-89.186759948730469","Height":"106.40826416015625","Width":"25.875263214111328","Left":2391.4501953125}}]},"RequestId":"BB5564E2-8AD0-4EF1-9F8B-0551A107033B"}'
    return json.loads(respStr)["Data"]["Results"]

def detectVehicle(imgUrl):
    client = AcsClient(accessKeyId, accessSecret, 'cn-shanghai')
    request = DetectVehicleRequest()
    request.set_accept_format('json')
    request.set_ImageURL(imgUrl)
    response = client.do_action_with_exception(request)
    respStr = str(response, encoding='utf-8')
    # respStr = '{"Data":{"Height":822,"DetectObjectInfoList":[{"Boxes":[605,343,998,644],"Type":"vehicle","Id":0,"Score":0.935}],"Width":1494},"RequestId":"6E2F7080-3D00-4055-828F-E2CC6D73DD9C"}'
    return json.loads(respStr)["Data"]["DetectObjectInfoList"]

def recognizeVehicleParts(imgUrl):
    client = AcsClient(accessKeyId, accessSecret, 'cn-shanghai')
    request = RecognizeVehiclePartsRequest()
    request.set_accept_format('json')
    request.set_ImageURL(imgUrl)
    response = client.do_action_with_exception(request)
    respStr = str(response, encoding='utf-8')
    return json.loads(respStr)["Data"]["Elements"]

def getImgSize(imgPath:str) -> dict:
    im = Image.open(imgPath)
    imgSize = dict()
    imgSize["width"] = im.size[0]
    imgSize["height"] = im.size[1]
    return imgSize

def cropImg(imgPath, box) -> str:
    im = Image.open(imgPath)
    cropped = im.crop(box)
    output = os.path.dirname(os.path.abspath(imgPath))+'/cropped_'+str(random.randint(0,100))+'_'+os.path.basename(imgPath)
    cropped.save(output)
    return output
    
