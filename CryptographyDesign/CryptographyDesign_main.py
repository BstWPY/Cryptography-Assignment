'''                     
                         密码学大作业
关于Logistic,Singer,Iterative混沌映射生成的置乱表性能评测及图像加密应用
         学号:PB22061233              姓名:王鹏宇
'''
import math
'''
首先先对N确定的情况进行评测,这里选取3个参数和3个初始值作为种子,每种映射生成
9个置乱表
'''
A=[3.7,3.8,3.9]#Logistic混沌映射参数
B=[0.96,1.0,1.06]#Singer混沌映射参数
C=[0.5,0.7,0.9]#Iterative混沌映射参数
X=[0.24,0.51,0.83]#Logistic初始值
Y=[0.26,0.51,0.75]#Singer初始值
Z=[-0.26,0.26,0.5]#Iterative初始值
N=512
def Logistic(x,o):#Logistic混沌映射
    return o*x*(1-x)
def Singer(x,o):#Singer混沌映射
    return o*(7.86*x-23.31*x*x+28.75*x*x*x-13.302875*x*x*x*x)
def Iterative(x,o):#Iterative混沌映射
    return math.sin(o*math.pi/x)
#储存迭代1000轮的值
xm=[]
ym=[]
zm=[]
#继续迭代N次的值
xn=[{},{},{},{},{},{},{},{},{}]
yn=[{},{},{},{},{},{},{},{},{}]
zn=[{},{},{},{},{},{},{},{},{}]
#迭代求M次的值
for i in range(3):#迭代求Logistic的Xm
    for j in range(3):
        xm.append(Logistic(X[j],A[i]))#先迭代一次
        for k in range(999):
            xm[i*3+j]=Logistic(xm[i*3+j],A[i])#继续迭代获得XM
for i in range(3):#迭代求Singer的Ym
    for j in range(3):
        ym.append(Singer(Y[j],B[i]))#先迭代一次
        for k in range(999):
            ym[i*3+j]=Singer(ym[i*3+j],B[i])#继续迭代获得XM
for i in range(3):#迭代求Iterative的Zm
    for j in range(3):
        zm.append(Iterative(Z[j],C[i]))#先迭代一次
        for k in range(999):
            zm[i*3+j]=Iterative(zm[i*3+j],C[i])#继续迭代获得XM

for i in range(3):#迭代N轮的初始值
    for j in range(3):
        xn[i*3+j].update({0:Logistic(xm[i*3+j],A[i])})
for i in range(3):
    for j in range(3):
        yn[i*3+j].update({0:Singer(ym[i*3+j],B[i])})
for i in range(3):
    for j in range(3):
        zn[i*3+j].update({0:Iterative(zm[i*3+j],C[i])})
#正式开始迭代(N确定)
for i in range(9):
    for j in range(1,N):
        xn[i].update({j:Logistic(xn[i][j-1],A[i//3])})
for i in range(9):
    for j in range(1,N):
        yn[i].update({j:Singer(yn[i][j-1],B[i//3])})
for i in range(9):
    for j in range(1,N):
        zn[i].update({j:Iterative(zn[i][j-1],C[i//3])})         
#从小到大排序
xs=[[],[],[],[],[],[],[],[],[]]
ys=[[],[],[],[],[],[],[],[],[]]
zs=[[],[],[],[],[],[],[],[],[]]
for i in range(9):
    xs[i]=sorted(xn[i].items(),key=lambda s:s[1])
    ys[i]=sorted(yn[i].items(),key=lambda s:s[1])
    zs[i]=sorted(zn[i].items(),key=lambda s:s[1])
#构造置乱表
tmp=0.0
for i in range(9):
    for j in range(N):#遍历xn
        for k in range(N):#遍历xs
            if xs[i][k][0]==j:
                xn[i].update({j:k})
for i in range(9):
    for j in range(N):#遍历yn
        for k in range(N):#遍历ys
            if ys[i][k][0]==j:
                yn[i].update({j:k})
for i in range(9):
    for j in range(N):#遍历yn
        for k in range(N):#遍历ys
            if zs[i][k][0]==j:
                zn[i].update({j:k})
print(xn[0])
#初始化循环阶数
countx=[{},{},{},{},{},{},{},{},{}]
county=[{},{},{},{},{},{},{},{},{}]
countz=[{},{},{},{},{},{},{},{},{}]
#循环阶数计算
for i in range(9):  
    while True:
        tmpkey=next(iter(xn[i]))
        begin=-1
        j=1#循环的阶数初始化
        tmpvalue=xn[i][tmpkey]
        while True:
            if begin==-1:#记录初始的置换
                begin=tmpkey           
            tmpvalue=xn[i][tmpkey]
            del xn[i][tmpkey]
            if tmpvalue==begin:#发现循环
                try:
                    countx[i].update({j:countx[i][j]+1})
                except KeyError:
                    countx[i].update({j:1})
                break        
            tmpkey=tmpvalue           
            j=j+1
        if len(xn[i])==0:
            break

for i in range(9):  
    while True:
        tmpkey=next(iter(yn[i]))
        begin=-1
        j=1#循环的阶数初始化
        tmpvalue=yn[i][tmpkey]
        while True:
            if begin==-1:#记录初始的置换
                begin=tmpkey           
            tmpvalue=yn[i][tmpkey]
            del yn[i][tmpkey]
            if tmpvalue==begin:#发现循环
                try:
                    county[i].update({j:county[i][j]+1})
                except KeyError:
                    county[i].update({j:1})
                break        
            tmpkey=tmpvalue           
            j=j+1
        if len(yn[i])==0:
            break
for i in range(9):  
    while True:
        tmpkey=next(iter(zn[i]))
        begin=-1
        j=1#循环的阶数初始化
        tmpvalue=zn[i][tmpkey]
        while True:
            if begin==-1:#记录初始的置换
                begin=tmpkey           
            tmpvalue=zn[i][tmpkey]
            del zn[i][tmpkey]
            if tmpvalue==begin:#发现循环
                try:
                    countz[i].update({j:countz[i][j]+1})
                except KeyError:
                    countz[i].update({j:1})
                break        
            tmpkey=tmpvalue           
            j=j+1
        if len(zn[i])==0:
            break
#计算阶                
countx1=[]
county1=[]
countz1=[]
for i in range(9):
    tmp=1
    if len(countx[i])==1:
            countx1.append(N)
            continue
    for key in countx[i]:       
        tmp=math.lcm(tmp,key)
    countx1.append(tmp)
for i in range(9):
    tmp=1
    if len(county[i])==1:
            county1.append(N)
            continue
    for key in county[i]:       
        tmp=math.lcm(tmp,key)
    county1.append(tmp)
for i in range(9):
    tmp=1
    if len(countz[i])==1:
            countz1.append(N)
            continue
    for key in countz[i]:       
        tmp=math.lcm(tmp,key)
    countz1.append(tmp)
#计算平均阶
avecountx=int(sum(countx1)/len(countx1))
avecounty=int(sum(county1)/len(county1))
avecountz=int(sum(countz1)/len(countz1))
print(avecountx)
print(avecounty)
print(avecountz)