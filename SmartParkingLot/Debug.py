import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from matplotlib.transforms import Affine2D
import numpy as np
import LotUtils


def showImgWithRect(imgPath, rectArr):
    im = np.array(Image.open(imgPath), dtype=np.uint8)
    # Create figure and axes
    fig,ax = plt.subplots(1)
    ts = ax.transData
    # Display the image
    ax.imshow(im)
    for item in rectArr:
        trans = Affine2D().rotate_deg_around(item["left"]+(item["width"]/2),item["bottom"]+(item["height"]/2),item["angle"])
        t = trans + ts
        ax.add_patch(patches.Rectangle((item["left"],item["bottom"]),item["width"],item["height"],linewidth=2,edgecolor='yellow',facecolor='none',transform=t))
    plt.show()

imgName = "illegalPark_2.jpg"
imgPath = os.path.dirname(os.path.abspath(__file__))+'/'+imgName
imgUrl = LotUtils.uploadImg(imgPath)
# show recognize rectangles
charRes = LotUtils.recognizeCharacter(imgUrl)
vehiRes = LotUtils.detectVehicle(imgUrl)
rectArr = []
for item in charRes:
    rect = dict()
    rect["left"] = int(float(item["TextRectangles"]["Left"]))
    rect["bottom"] = int(float(item["TextRectangles"]["Top"]))
    rect["width"] = int(float(item["TextRectangles"]["Width"]))
    rect["height"] = int(float(item["TextRectangles"]["Height"]))
    rect["angle"] = float(item["TextRectangles"]["Angle"])
    rectArr.append(rect)
'''    
for item in vehiRes:
    rect = dict()
    rect["left"] = item["Boxes"][0]
    rect["bottom"] = item["Boxes"][1]
    rect["width"] = item["Boxes"][2]-item["Boxes"][0]
    rect["height"] = item["Boxes"][3]-item["Boxes"][1]
    rect["angle"] = 0
    rectArr.append(rect)
'''
    
showImgWithRect(os.path.dirname(os.path.abspath(__file__))+'/'+imgName,rectArr)