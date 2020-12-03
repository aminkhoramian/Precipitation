# import numpy as np
# import h5py
# import matplotlib.pyplot as plt
# from rasterio.plot import show
# pcp = h5py.File('D:/Users/khoramian.a/Downloads/3B', 'r')
# pcp=pcp['Grid']
# pcp=pcp['precipitationCal']
# pcp=np.array(pcp)
# pcp=pcp[0,::,::]
# cn=pcp[0,0]
# pcp = np.where(pcp == cn, np.nan, pcp)

# # for i in pcp:
# #     for j in i:
# #         if j<-999:
# #             j=np.nan
            
# # plt.imshow(pcp)
# # plt.show()
# show(pcp)
import datetime
import math
import requests
import json
import os
from shutil import copyfile
from PCPfunctions import maskingfiles

st_date=[2020,11,29,7,25]
end_date=[2020,11,29,23,35]
st=datetime.datetime(st_date[0],st_date[1],st_date[2],st_date[3],st_date[4])
ed=datetime.datetime(end_date[0],end_date[1],end_date[2],end_date[3],end_date[4])
diff=ed-st
steps=diff.seconds/(60*30)
# intitae first time step and steps count
st=st.replace(minute=30*math.floor(st.minute/30))
steps=math.floor(steps)
stp_date=st
#

    
#API request
apiresponse = requests.get('https://pmmpublisher.pps.eosdis.nasa.gov/opensearch?q=precip_30mn&lat=33&lon=53&limit=100&startTime=' + str(st_date[0]) + '-' + str(st_date[1]).zfill(2) + '-' + str(st_date[2]).zfill(2) + '&endTime=' + str(end_date[0]) + '-' + str(end_date[1]).zfill(2) + '-' + str(end_date[2]).zfill(2))
jsondic=json.loads(apiresponse.text)
del apiresponse
for i in range (0,jsondic['totalItems']):
    print(i)
    api_folder_name=jsondic['items'][i]['properties']['date']['@value']
    api_folder_name='api/'+api_folder_name[0:4]+api_folder_name[5:7]
    file_name=jsondic['items'][i]['@id']+'.tif'
    api_path_name=api_folder_name+'/'+file_name
    DB_folder_name='DB/'+api_folder_name[4:8]+api_folder_name[8:10]
    DB_path_name=DB_folder_name+'/'+file_name
    #Checking file exist in DB folder or not and if not download it
    if not os.path.isfile(DB_path_name):
        adress=jsondic['items'][i]['action'][1]['using'][1]['url']
        req = requests.get(adress)
        if not os.path.exists(api_folder_name):
            os.makedirs(api_folder_name)        
        with open(api_path_name, 'wb') as f:
            f.write(req.content)
        del adress, req, f
        # Make a copy to DB folder
        if not os.path.exists(DB_folder_name):
            os.makedirs(DB_folder_name)
        copyfile(api_path_name, DB_path_name)
#


#Getting remainings from ftp server

# ftp request
for i in range(0,steps):
    print(i)
    stp2_date=stp_date+datetime.timedelta(seconds=59,minutes=29)
    file_name='gpm_30mn_'+str(stp2_date.year)+str(stp2_date.month).zfill(2)+str(stp2_date.day).zfill(2)+ '_'  + str(stp2_date.hour).zfill(2)+str(stp2_date.minute).zfill(2) + str(stp2_date.second).zfill(2) + '.tif'
    BD_folder_name='DB/'+str(stp2_date.year)+str(stp2_date.month).zfill(2)
    ftp_folder_name='ftp/'+str(stp2_date.year)+str(stp2_date.month).zfill(2)
    DB_path_name=DB_folder_name + '/' + file_name
    ftp_path_name=ftp_folder_name + '/' + file_name
    # 3B-HHR-E.MS.MRG.3IMERG.20201101-S003000-E005959.0030.V06B.RT-H5
    if not os.path.isfile(DB_path_name):
        digi=str((math.floor((stp_date.hour*60+stp_date.minute)/30))*30).zfill(4)
        file_url='https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/gis/early/'+ str(stp_date.year) + '/' + str(stp_date.month).zfill(2) + '/3B-HHR-E.MS.MRG.3IMERG.' + str(stp_date.year) + str(stp_date.month).zfill(2) + str(stp_date.day).zfill(2) + '-S' + str(stp_date.hour).zfill(2) + str(stp_date.minute).zfill(2) + str(stp_date.second).zfill(2) + '-E' + str(stp2_date.hour).zfill(2) + str(stp2_date.minute).zfill(2) + str(stp2_date.second).zfill(2) + '.' + digi + '.V06B.30min.tif'
        with requests.Session() as session:
            req = session.request('get', file_url)
            r = session.get(req.url, auth=('khoramian.a@gmail.com', 'khoramian.a@gmail.com'))
            if not os.path.exists(ftp_folder_name):
                os.makedirs(ftp_folder_name)
            with open(ftp_path_name, 'wb') as f:
                f.write(r.content)
        del r, req, f
        maskingfiles(ftp_path_name,DB_path_name)
    # else:
    #     copyfile(src, dst)
    stp_date=stp_date+datetime.timedelta(minutes=30)
            

