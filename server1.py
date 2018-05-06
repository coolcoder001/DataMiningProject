import pandas as pd
import numpy as np
ans_count= pd.read_csv('Ans_count.csv')
# print((ans_count))
from collections import defaultdict
ans_count_dict=defaultdict(int)
for i in range(ans_count.size):
    ans_count_dict['UserId']= 'count(p.Id)'
AnsGroup = ans_count.groupby('UserId')
UsrAnsKeys = AnsGroup.groups.keys()    
for user in UsrAnsKeys:
    ans_count_dict[user]= AnsGroup.get_group(user).values[:,1:][0][0]
ans_list = pd.read_csv('Ans_List.csv')
from collections import defaultdict
outer_dict=defaultdict(int)
# inner_dict=defaultdict(int)
dd = (ans_list['Id'].unique())
# print((dd))
usrkeys= ans_list.groupby('UserId').groups.keys()
usr_dict= defaultdict(int)
usrCount=len(usrkeys)
usrDimension = (usrCount,usrCount)
import math
usrmatrix=np.zeros(usrDimension)
print(usrCount)
count=0
for i in usrkeys:
    usr_dict[i]=count
    count+=1
# print(usr_dict)    
# count=0
usr_dict1=defaultdict(int)
for i,j in zip(range(usrCount),usrkeys):
#     print(" i ",i," j ",j)
    usr_dict1[i]=j
    #count+=1
for i in dd:
    user_list=[]
    df1 = ans_list[ans_list['Id']==i]['UserId']
    df1_count = df1.count()
#     if(i == 54):
#         break
#     inner_dict=defaultdict(int)
    if(df1_count<2):
        continue
    else:
        for j in df1:
            user_list.append(j)
#             count=0
        for ii in range(0,len(user_list)-1):
#             print(outer_dict)
            for jj in range(ii+1,len(user_list)):
#                 inner_dict=defaultdict(int)
                num1=user_list[ii]
                num2=user_list[jj]
                usrmatrix[usr_dict[num1]][usr_dict[num2]]+=1
                usrmatrix[usr_dict[num2]][usr_dict[num1]]+=1
for kk in range(len(usrmatrix)):
    usrmatrix[kk][kk]=1
usr_comp_mtx_refine= np.copy(usrmatrix)
row_count=0
row_trace=[]
for n in usrmatrix:
    if(np.sum(n)==0):
        row_trace.append(row_count)
    row_count+=1  
# row_count
usr_comp_mtx_refine.shape
usr_comp_mtx_refine=np.delete(usr_comp_mtx_refine,row_trace,0)
usr_comp_mtx_refine.shape
usr_comp_mtx_refine=usr_comp_mtx_refine.transpose()
row_count=0
row_trace=[]
for n in usr_comp_mtx_refine:
    if(np.sum(n)==0):
        row_trace.append(row_count)
    row_count+=1  
# row_count    
usr_comp_mtx_refine=np.delete(usr_comp_mtx_refine,row_trace,0)
z1,z2=usr_comp_mtx_refine.shape
# print(z1,z2)
import math
for i in range(0,z1-1):
    for j in range(i+1,z1):
        var1=ans_count_dict[usr_dict1[i]]
        var2=ans_count_dict[usr_dict1[j]]
        usr_comp_mtx_refine[i][j]=usr_comp_mtx_refine[j][i]=usr_comp_mtx_refine[i][j]/(math.sqrt(var1*var2))
usr_comp_inv1= np.copy(usr_comp_mtx_refine)
for p1 in usr_comp_inv1:
    for p2 in range(len(p1)):
        if(p1[p2]==0):
            p1[p2]=999
        else:
            p1[p2]=1/p1[p2]
# print(usr_comp_inv1)            
from  scipy.sparse.csgraph import floyd_warshall as fw
from  scipy.sparse.csgraph import shortest_path as sp
dis_mtx = sp(usr_comp_inv1,method='auto',directed=False)
a = np.asarray(dis_mtx)
np.savetxt("/home/cs18mtech01004/DataMining/output1.csv", a, delimiter=",")


                    