# 智能停车场

## [赛题链接](https://tianchi.aliyun.com/competition/entrance/231769/introduction)

## 场景描述
现在大型商超、医院、公园、景区等公共场所都配备大型停车场。在人流密集的区段前往时，车主们往往需要在停车场里来回兜圈寻找空余停车位，消耗时间，影响心情。在离开时，又可能因为忘记停车位置而大海捞针。目前停车场会在车主入场时告知，剩余停车位数量，而无具体位置。更无法在车主离场时提供爱车车位。<br/>
该作品可同时解决上述两大问题，在车主入场时，实时告知车主目前空闲停车位ID。在车主离场时，根据车牌号，找出停车位置，节省车主找车时间，提高停车位使用效率。

## 作品简介
该作品借助阿里云视觉智能平台，旨在解决大型停车场两大难
- 入场时，寻找车位难
- 离场时，定位目标车辆难

以摄像头提供静态画面为输入，提供三大核心功能：
1. 寻找空闲停车位
2. 检查不规范停车方式（即横向停车）
3. 通过车牌号定位车辆信息

## Dependency
included in requirements.txt
### Python
- Python 3.7
### packages
- oss2 (`pip3 install oss2`)
- PIL (`pip3 install Pillow`)
- aliyun-python-sdk-core-v3 (`pip3 install aliyun-python-sdk-core-v3`)
- aliyun-python-sdk-objectdet(`pip3 install aliyun-python-sdk-objectdet`)
- aliyun-python-sdk-ocr(`pip3 install aliyun-python-sdk-ocr`)

### 阿里视觉智能平台API
1. 目标检测
2. 车辆检测
3. 文字识别
4. 车辆部件识别

### 阿里平台其他功能
1. OSS
2. Terraform
3. ECS

## 部署流程

### Docker方式
```bash
$pwd
/Users/fuwq/Documents/notes/SmartParkingLot

$ls
Aliyun_AI_application.md	dataset
AnalysisLot.py			img
Debug.py			index.html
Dockerfile			lotAnalyst.html
LocateCar.py			portal.py
LotUtils.py			requirements.txt
README.md			runDocker.sh
carLocator.html			terraform_oss

$docker build --tag smartparkinglot:1.0 .

$docker run --publish 80:8080 --detach --name SPL smartparkinglot:1.0

```

### 非Docker方式
```bash
$pwd
/Users/fuwq/Documents/notes/SmartParkingLot

$ls
Aliyun_AI_application.md	dataset
AnalysisLot.py			img
Debug.py			index.html
Dockerfile			lotAnalyst.html
LocateCar.py			portal.py
LotUtils.py			requirements.txt
README.md			runDocker.sh
carLocator.html			terraform_oss

$python3 portal.py
Server started http://localhost:8080

```

## 文件目录
### Aliyun_AI_application.md
初赛复赛内容准备说明。

### dataset
功能验证和展示所需的图片，在打开[分析现有停车位](http://47.116.104.65/lotAnalyst.html) 和 [定位车辆位置](http://47.116.104.65/carLocator.html)页面后，可将该文件夹下任一图片上传加以验证。

### img
上传文件的临时存储区。

### terraform_oss
terraform 脚本，在 **cn-shanghai** region 创建 **bucket-20200322-2** bucket，供上传图片。

### Py文件

- [AnalysisLot.py](./AnalysisLot.py)。提供停车位分析功能。分析是否有停车位，是否存在不规范停车行为。
- [LocateCar.py](./LocateCar.py)。提供车辆定位功能。分析输入的车牌号是否在图片中存在，若存在则识别对应的停车位ID。
- [LotUtils.py](./LotUtils.py)。各种工具方法。
- [Debug.py](./Debug.py)。提供Debug功能，依赖matplotlib，numpy。
- [portal.py](./portal.py)。提供localhost页面，展示上述功能。

### Html文件
- index.html。Home page
- lotAnalyst.html。停车位分析功能展示页。
- carLocator.html。车辆定位功能展示页。

## 核心功能介绍
### 空闲停车位查找（入口函数参见`AnalysisLot.findEmptyParkingLots`）

1. 借助**文字识别**能力中`RecognizeCharacter`技术，识别停车场照片中的所有文字
2. 以正则匹配的方式识别出停车位ID文字，参见`LotUtils.isParkingLotsText`实现
3. 借助**目标检测**能力中`DetectVehicle`技术，检测照片中所有的车辆，提取出Box数据信息
4. 通过车辆Box数据计算出车辆的width, height，计算两者比值，及其与图片大小的比值，排除无关车辆，参见`LotUtils.isNoiseCar`实现
5. 计算剩余有效车辆的中心点与停车位ID文字框中心点的距离，择其最近的ID文字框作为该辆车所占据的停车位。参见`AnalysisLot.findNearestLot`实现
6. 计算第2步所有停车位ID 与 第5步被占用停车位ID 的差值，得到空闲停车位数据
7. 补充说明，若照片中没有停车位ID，则默认单一摄像头覆盖3个停车位。现实中可将其作为参数由使用者指定。借由摄像头位置反映空闲停车位坐标。

### 不规范停车（即横向停车）发现（入口函数参见`AnalysisLot.findIllegalParking`）

1. 借助**目标检测**能力中`DetectVehicle`技术，检测照片中所有的车辆，提取出Box数据信息
2. 考虑到正常停车方式为纵向，width一般小于或等于height。计算车辆width、height，若width >= 1.5 * height，进行下一步检测，否则认为该车停车规范。
3. 考虑到如果是横向停车，摄像头则只能拍到车辆的左面/右面。借助**目标检测**能力中`RecognizeVehicleParts`技术，检测图片中车辆零部件。轮询返回结果中Elements，分别统计*left-*, *right-*作为prefix的结果数量
4. 计算两者差值的绝对值，若大于7，则判定存在不规范停车。若无，则继续判定下一车辆。参见`AnalysisLot.judgeIllegalParking`实现。

### 车辆定位（入口函数参见`LocateCar.locateMyCar`）

1. 借助**文字识别**能力中`RecognizeCharacter`技术，识别停车场照片中的所有文字
2. 以正则匹配的方式识别出停车位ID文字，参见`LotUtils.isParkingLotsText`实现
3. 对识别结果剩余文字，逐一计算与目标车牌号的相似度，参见`LocateCar.computeSimilarity`实现。为兼容识别可能出现不准确的情况，将所有相似度超过70%的车牌号输入下一步。若所有文字与目标车牌相似度均未达标，则返回该照片中无目标车辆。
4. 计算第3步得到的疑似文字框与第2步停车位ID文字中心点之间的距离，择其最短距离者作为目标车辆位置，并返回。
5. 若图片中无停车位ID，则跳过第4步，直接返回"Target Car is here, but no Lot ID"。借由摄像头位置反映目标车辆坐标。

## 作品总结

### 技术方案总结
基于阿里云视觉智能平台成熟的车辆检测、文字识别、车辆部件识别等能力，将AI视觉能力引入大型公共停车场领域，提升车主客户体验。<br/>
加入相似度计算以增加容错能力，更贴近实际场景，降低落地门槛。<br/>
支持Docker化部署，减少部署成本，可自由动态扩容。

### VS 行业成熟方案
||[地磁技术方案](http://www.libelium.com/products/smart-parking/)|智能方案|[超声波车位探测技术](https://www.smartparking.com/smartpark-system/smart-sensors)|
|--|--|--|--|
|设备依赖|具有雷达/磁场发射功能的传感器|相对清晰的监控摄像头|置于车位上方的摄像头|
|设备覆盖范围|1 车位/个|3-5 车位/个|3-5 车位/个|
|识别准确率|高|较高，依赖于摄像头分辨率及算法优化|高|
|功能|1. 空闲车位数量及位置|1. 空闲车位数量及定位<br>2. 发现不规范停车行为<br>3. 指定车辆位置|1. 空闲车位数量及位置|
|部署难易|国内停车场较少，需采购部署。且每个停车位需部署一个传感器，成本很高|国内停车场基本部有摄像头，可直接使用。成本很低|需在高位新增架设摄像头|
|迭代难易|传感器更新换代，需重新采购安装|云端部署服务，敏捷开发，轻易迭代|受限于信息采集，较小迭代空间|

### 前景价值

以下内容来自[《2018年中国停车行业发展白皮书》](http://dy.163.com/v2/article/detail/EGP453H10519C1CN.html)，有删减。

>截至2018年底，我国内地机动车保有量突破3.27亿辆，其中小汽车保有量突破2.4亿，私家车保有量突破1.89亿辆。在内地主要城市中，北京市的汽车保有量最多，为608.4万辆，备案停车位总数189.05万个。深圳汽车保有量336.66万，停车位145万个。

智能停车场方案，可基于停车场已安装的摄像头，对每个大城市数百万的停车位同时进行分析，节省百万车主在停车场苦苦寻找停车位的时间。以北京为例，假设每位车主每次寻找停车位的时间是5分钟，一周2次，那么智能停车场方案为每位北京车主节省的时间就是 5min * 2次 * 52周 = 520 min。为全北京市车主节省的可是 520 min * 608.4万 = 316368 万分钟 = 5272.8 万小时 = 219.7 万天。
