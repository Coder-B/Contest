import os
import math
import LotUtils

class CarLocator:
    # 计算识别获得文字与目标车牌的相似度
    # 考虑到数字和字母识别效果好于汉字，仅比对数字和字母，且采用从后往前的顺序进行匹配。
    # 出现不匹配的字符立即停止比对，计算相同字符串长度所占比例作为相似度输出
    def computeSimilarity(self, inputText:str , recogText:str) -> float:
        sameLetter = 0
        processedRecoText = LotUtils.extractNormalWords(recogText)
        for i in range(0,min(len(inputText), len(processedRecoText))):
            if inputText[-1-i] == processedRecoText[-1-i]:
                sameLetter+=1
            else:
                break
        return sameLetter/len(inputText)


    def locateMyCar(self, carnumber, charRes):
        res = {}
        res["recogText"] = []
        plat = []
        for item in charRes:
            res["recogText"].append(item["Text"])
            if LotUtils.isParkingLotsText(item["Text"]):
                continue
            if self.computeSimilarity(carnumber,item["Text"]) >= 0.7:
                plat.append(item)
        if len(plat) == 0:
            res["location"] = ["No target car here"]
        else:
            lots = []
            hasLotId = False
            for platItem in plat:
                platCenter = LotUtils.getCharBoxCenter(platItem)
                nearestLot,minDistanceSq = "",math.pow(self.imgSize["width"],2)+math.pow(self.imgSize["height"],2)
                for item in charRes:
                    if LotUtils.isParkingLotsText(item["Text"]):
                        hasLotId = True
                        lotCenter = LotUtils.getCharBoxCenter(item)
                        xDistance,yDistance = platCenter[0]-lotCenter[0],platCenter[1]-lotCenter[1]
                        distanceSq = math.pow(xDistance,2)+math.pow(yDistance,2)
                        if distanceSq < minDistanceSq:
                            minDistanceSq = distanceSq
                            nearestLot = item["Text"]
                lots.append(nearestLot)
            if hasLotId:
                res["location"] = lots
            else:
                res["location"] = ["Target Car is here, but no Lot ID"]
        return res

    def locateCar(self, plateNum):
        imgUrl = LotUtils.uploadImg(self.imgPath)
        charRes = LotUtils.recognizeCharacter(imgUrl)
        return self.locateMyCar(plateNum, charRes)

    def __init__(self, imgPath):
        super().__init__()
        self.imgPath = imgPath
        self.imgSize = LotUtils.getImgSize(imgPath)

'''
imgName = "carsInLot.png"
imgPath = os.path.dirname(os.path.abspath(__file__))+'/'+imgName
imgSize = LotUtils.getImgSize(imgPath)
imgUrl = LotUtils.uploadImg(imgPath)
charRes = LotUtils.recognizeCharacter(imgUrl)
print("find your car with plat \"辽A999P2\" at "+str(locateMyCar("辽A999P2",charRes)))
'''