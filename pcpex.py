# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:12:36 2020

@author: khoramian.a
"""

import numpy as np
import h5py
import matplotlib.pyplot as plt
pcp = h5py.File('D:/PCP/aminoo', 'r')
pcp=pcp['Grid']
pcp=pcp['precipitationCal']
pcp=np.array(pcp)
pcp=pcp[0,::,::]
cn=pcp[0,0]
pcp = np.where(pcp == cn, np.nan, pcp)

            
plt.imshow(pcp)
plt.show()

