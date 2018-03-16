# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:36:38 2018
examples for management of hdf5 file.
@author: jyr_king
"""
import h5py as h5
import numpy as np
import time
#创建一个hdf5数据文件并打开它，同时添加一些基本信息（元数据）
f1=h5.File('mytesth5.h5','w')
f1.attrs['discription']='a hdf5 for demonstration.'
f1.attrs['create time']=time.time()
f1.attrs['author']='Somebody'

#添加一个group
g1=f1.create_group('grp1')
#在g1中添加一个数据（dataset）
g1.create_dataset('dset1',data=np.arange(100),dtype='f8')
dset1=g1['dset1']
dset1.dtype

dset1.attrs['discription']='my measurement'
dset1.attrs['create time']=time.time()
dset1.attrs['sample_rate']=1e6
dset1.attrs['Unit']='mV'

#保存数据但不关闭文件
f1.flush()

#修改数据
dset1[...]=np.ones(dset1.shape)
dset1[::2]=3
