import math
import os
import LotUtils

class LotAnalyst:
    MAX_LOTS = 3
    def calculateDistance(self, vehicleBox, lot):
        lotCenter = LotUtils.getCharBoxCenter(lot)
        # vertical distance
        # the bottom of vehicle and the center of lot ID
        yDistance = vehicleBox[3]-(float(lot["TextRectangles"]["Top"])+float(lot["TextRectangles"]["Height"])/2)
        # the center of vehicle and the center of lot ID
        xDistance = (vehicleBox[0]+vehicleBox[2])/2-lotCenter[0]
        return xDistance*xDistance+yDistance*yDistance

    def findNearestLot(self, vehicleBox, parkingLots):
        nearestLot,minDistance = "",math.pow(self.imgSize["width"],2)+math.pow(self.imgSize["height"],2)
        for item in parkingLots:
            if LotUtils.isParkingLotsText(item["Text"]):
                distance = self.calculateDistance(vehicleBox,item)
                if distance < minDistance:
                    minDistance = distance
                    nearestLot = item["Text"]
        # print("nearestLot is ",item["Text"],", distance is: ",math.sqrt(distance))
        return nearestLot

    # judge if some text is car plate by compare the location with vehicle's
    def isPlate(self, charBox, vehicleBoxList):
        if not LotUtils.isParkingLotsText(charBox["Text"]):
            charCenter = LotUtils.getCharBoxCenter(charBox)
            for item in vehicleBoxList:
                vehicleCenter = [(int(item["Boxes"][0])+int(item["Boxes"][2]))/2, (int(item["Boxes"][1])+int(item["Boxes"][3]))/2]
                distance = [charCenter[0]-vehicleCenter[0],charCenter[1]-vehicleCenter[1]]
                if distance[0]<(int(item["Boxes"][2])-int(item["Boxes"][0]))/2 and distance[1]<(int(item["Boxes"][3])-int(item["Boxes"][1]))/2:
                    return True
        return False


    def findEmptyParkingLots(self, charRes,vehicleRes):
        print("Searching available lots ...")
        allLots = dict()
        for item in charRes:
            if LotUtils.isParkingLotsText(item["Text"]):
                allLots[str(item["Text"])] = 1
        print("allLots: ", allLots)
        availableLots = []
        if len(allLots) > 0:
            for item in vehicleRes:
                nearestLot = self.findNearestLot(item["Boxes"],charRes)
                print("try to delLot: ",str(nearestLot))
                if str(nearestLot) in allLots:
                    del allLots[str(nearestLot)]
            availableLots = list(allLots.keys())
        else:
            availableLots = ["1" for i in range(0, max(0,self.MAX_LOTS - len(vehicleRes)))]
        print(availableLots)
        return availableLots

    def judgeIllegalParking(self, imgUrl):
        elements = LotUtils.recognizeVehicleParts(imgUrl)
        leftcnt, rightcnt = 0,0
        for item in elements:
            if item['Score'] > 0.75:
                if item['Type'][:5] == 'left_':
                    leftcnt += 1
                elif item['Type'][:5] == 'right':
                    rightcnt += 1
        if abs(leftcnt-rightcnt) > 7:
            return True
        else:
            return False


    def findIllegalParking(self, vehiRes):
        print("Scanning illegal parking...")
        result = "All parking are legal"
        for item in vehiRes:
            width = item["Boxes"][2]-item["Boxes"][0]
            height = item["Boxes"][3]-item["Boxes"][1]
            if width >= 1.5 * height:
                croppedPath = LotUtils.cropImg(self.imgPath,item["Boxes"])
                imgUrl = LotUtils.uploadImg(croppedPath)
                os.remove(croppedPath)
                if self.judgeIllegalParking(imgUrl):
                    result = "Illegal Parking Exists"
                    break
        return result

    def analysisLot(self):
        print("begin analysisLot ...")
        imgUrl = LotUtils.uploadImg(self.imgPath)
        charRes = LotUtils.recognizeCharacter(imgUrl)
        vehiRes = LotUtils.detectVehicle(imgUrl)
        effectiveVehiRes = []
        for item in vehiRes:
            if not LotUtils.isNoiseCar(item, self.noiseCarThreshold["minWidth"], self.noiseCarThreshold["minHeight"]):
                effectiveVehiRes.append(item)
        report = {}
        report["availableLots"] = self.findEmptyParkingLots(charRes,effectiveVehiRes)
        report["illegalPark"] = self.findIllegalParking(effectiveVehiRes)
        return report

    def __init__(self, imgPath):
        self.imgPath = imgPath
        self.imgSize = LotUtils.getImgSize(imgPath)
        self.noiseCarThreshold = {}
        self.noiseCarThreshold["minWidth"] = self.imgSize["width"]/8
        self.noiseCarThreshold["minHeight"] = self.imgSize["height"]/3

'''
imgName = "illegalPark_2.jpg"
imgPath = os.path.dirname(os.path.abspath(__file__))+'/'+imgName
imgSize = LotUtils.getImgSize(imgPath)
imgUrl = LotUtils.uploadImg(imgPath)

charRes = LotUtils.recognizeCharacter(imgUrl)
vehiRes = LotUtils.detectVehicle(imgUrl)

# print("find available parking lots: ",self.findEmptyParkingLots(charRes,vehiRes))
print(self.findIllegalParking(vehiRes))
'''