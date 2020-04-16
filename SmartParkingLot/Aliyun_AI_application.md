[contest info](https://tianchi.aliyun.com/competition/entrance/231769/introduction)

# 初赛提交内容
1. 作品用途及应用场景<br>
    在商场、电影院等大型娱乐场所，有着大型停车场，开私家车进入的司机，往往在热闹时分会为寻找停车位而头疼不已。而在散场之后，又可能会因忘记停车位置而大海捞针。<br>
    智能停车场，利用停车场已有的监控摄像头，借助目标检测、文字识别等能力，帮助入场司机定位空余停车位，节省司机时间，避免场内车道拥堵。在司机准备离场时，提供车辆位置信息，无需专门留意停车位置，提升司机及家人在娱乐场所的体验。
2. 对应的用户群体
    所有为大型停车场体验而困扰的司机
3. 核心功能
    - 定位空余停车位
    - 寻找指定车辆位置
4. 应用技术
    - 目标检测
    - 车辆检测
    - 文字识别
5. 团队规模
    1人

# 复赛内容准备
1. 核心功能
    - 定位空余停车位
    - 检测不规范停车行为
    - 寻找指定车辆位置

2. 应用技术
    - 目标检测
    - 车辆检测
    - 文字识别
    - 车辆部件识别
    - Terraform生成OSS

3. VS 行业成熟方案

||传感器方案|智能方案|高位摄像头|
|--|--|--|--|
|设备依赖|具有雷达/磁场发射功能的传感器|相对清晰的监控摄像头|置于车位上方的摄像头|
|设备覆盖范围|1 车位/个|3-5 车位/个|3-5 车位/个|
|识别准确率|高|较高，依赖于摄像头分辨率及算法优化|高|
|功能|1. 空闲车位数量及位置|1. 空闲车位数量及定位<br>2. 发现不规范停车行为<br>3. 指定车辆位置|1. 空闲车位数量及位置|
|部署难易|国内停车场较少，需采购部署。且每个停车位需部署一个传感器，成本很高|国内停车场基本部有摄像头，可直接使用。成本很低|需在高位新增架设摄像头|
|迭代难易|传感器更新换代，需重新采购安装|云端部署服务，敏捷开发，轻易迭代|受限于信息采集，较小迭代空间|

4. 前景价值

以下内容来自[《2018年中国停车行业发展白皮书》](http://dy.163.com/v2/article/detail/EGP453H10519C1CN.html)

截至2018年底，我国内地机动车保有量突破3.27亿辆，其中小汽车保有量突破2.4亿，私家车保有量突破1.89亿辆。在内地主要城市中，北京市的汽车保有量最多，为608.4万辆，备案停车位总数189.05万个。深圳汽车保有量336.66万，停车位145万个。

智能停车场方案，可基于停车场已有的摄像头，对每个大城市数百万的停车位同时进行分析，节省数百万车主在停车场苦苦寻找停车位的时间。以北京为例，假设每位车主每次寻找停车位的时间是5分钟，一周5次，那么智能停车场方案为每位北京车主节省的时 间就是 5min * 5次 * 52周 = 1300 min。为全北京市车主节省的可是 1300 min * 608.4万 = 790920 万分钟 = 13182 万小时 = 549.25 万天 = 1.5 万年！