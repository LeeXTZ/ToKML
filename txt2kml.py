import numpy as np
import time

weight_list = []

def readTxt(path):  #读取txt文件
    coor_list = []
    print('reading txt...')
    with open(path,'r') as mytxt:
        mytxt.readline()  #略过第一行
        for line in mytxt.readlines():
            splitedline = line.split(',')
            # lng_list.append(splitedline[0])
            # lat_list.append(splitedline[1])
            lng = float(splitedline[0])
            lat = float(splitedline[1])
            coor = [lng,lat]
            coor_list.append(coor)
    sort_coor_list = sorted(coor_list)  #对坐标list进行排序
    print('txt read finish!')
    return sort_coor_list

# def calcuNum(coor_list):  #计算点周围的共享单车数量
#     # 114.275874, 30.628952 西北点
#     # 114.356901, 30.563269 中心点
#     # 114.437928, 30.497586 东南点
#     num_res_list = []
#     print('calculating num...')
#     for i_lng in np.arange(114.275,114.438,0.002):
#         for i_lat in np.arange(30.497,30.629,0.002):
#             max_lng = i_lng+0.002
#             min_lng = i_lng-0.002
#             max_lat = i_lat+0.002
#             min_lat = i_lat-0.002
#             num = 0
#             for i_coor in coor_list:
#                 if min_lng<i_coor[0]<max_lng and min_lat<i_coor[1]<max_lat:
#                     num += 1
#                 else:
#                     continue
#             num_res = [i_coor[0],i_coor[1],num]
#             num_res_list.append(num_res)
#     print('num calculatiion finish...')
#     return num_res_list

def calcuDmd(coor_list1,coor_list2):  # 调用calcuNum计算点周围的需求 
    dmd_res_list = []
    # num_res_list1 = calcuNum(coor_list1)
    # num_res_list2 = calcuNum(coor_list2)
    # for num_res1 in num_res_list1:
    #     for num_res2 in num_res_list2:
    #         print('calculating demand...')
    #         if num_res1[0]==num_res2[0] and num_res1[1]==num_res2[1]:
    #             dmd_res_list.append([num_res1[0],num_res1[1],num_res2[2]-num_res1[2]])
    # print('demand caculation finish!')

    # for i_lng in np.arange(114.275,114.438,0.001):
    #     for i_lat in np.arange(30.497,30.629,0.001):

    for i_lng,i_lat in coor_list1:   
        max_lng = i_lng+0.001
        min_lng = i_lng-0.001
        max_lat = i_lat+0.001
        min_lat = i_lat-0.001
        num1 = 0
        num2 = 0
        print('calculating demand...')
        for coor1 in coor_list1:
            if min_lng<coor1[0]<max_lng and min_lat<coor1[1]<max_lat:
                num1 += 1
            else:
                continue
        for coor2 in coor_list2:
            if min_lng<coor2[0]<max_lng and min_lat<coor2[1]<max_lat:
                num2 += 1
            else:
                continue
        if num1 > num2:
            dmd_res = [i_lng,i_lat, (num1-num2)]
            print('dmd_res:', dmd_res)
            dmd_res_list.append(dmd_res)
        else:
            continue
    print('demand caculation finish!')
    return dmd_res_list

def writeKml(drlist): 
    kml = '<Folder xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://www.opengis.net/kml/2.2">\n'
    for dmd_res in drlist:
        kml += ('  <Placemark>\n'+
        '    <demand>'+str(dmd_res[2])+'</demand>\n'+
        '    <Point>\n'+
        '      <coordinates>'+str(dmd_res[0])+','+str(dmd_res[1])+'</coordinates>\n'+
        '    </Point>\n'+
        '  </Placemark>\n')
        print('kml creating...')
    kml+='</Folder>'
    print('kml created successful!\nwriting into file...')
    with open('dmd0803.txt','w') as dmdtxt:
        dmdtxt.write(kml)

if __name__ =='__main__':
    mypath1 = '2017080310.txt'
    mypath2 = '2017080320.txt'

    start = time.strftime('%H:%M:%S',time.localtime())
    print('start from ',start)
    mycoor_list1 = readTxt(mypath1)
    mycoor_list2 = readTxt(mypath2)
    mydmd_res_list = calcuDmd(mycoor_list1,mycoor_list2)
    writeKml(mydmd_res_list)
    print('FINISH!')
    end = time.strftime('%H:%M:%S',time.localtime())
    print('end at ',end)
