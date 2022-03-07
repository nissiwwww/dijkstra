import csv
import time
import heapq
from numpy import zeros

##ファイル読み込み
max=float(10000)
f_in = open('ctr.txt', 'r')
datalist = f_in.readlines()

  ##時間
start_time = time.perf_counter()

onode = int(datalist[0])
print ("Origin",onode)
dnode = int(datalist[1])
print ("Destination",dnode)
link = datalist[2]
print ("Linkdata",link)
link_new = link.replace('\n', '')
output_file = datalist[3]
print ("Output file",output_file)
output_new = output_file.replace('\n', '')
f_out = open(output_new,'w',newline='\n')
f_in.close()

##本番
##リンクデータの読み込み
with open(link_new, encoding='utf8', newline='') as fe:
  reader = csv.reader(fe)
  header = next(reader)
  ss = [[int(row[2]), int(row[1]), int(row[4]),float(row[8])] if
  int(row[7]) ==1 else
  [int(row[1]), int(row[2]), int(row[4]),float(row[8])] for row in reader]
  content = [list(x) for x in zip(*ss)]
  tt = content[3]
  length = content[2]
  ##nodetable

  ldi1=[]
  ldi2=[]
  nodetable=[]
  ncm = [0]*15000
  nd = zeros((15000, 6))
  nmax=0
  i=0

  for t in ss:   ##ネック(c使うしかない)
    result = t[0] in nodetable
    if result == True:
      ind1 = nodetable.index(t[0])
      ldi1.append(ind1)
    else:
      nodetable.append(t[0])
      ldi1.append(nmax)
      nmax += 1
    ##node2も
    result = t[1] in nodetable
    if result == True:
      ind2 = nodetable.index(t[1])
      ldi2.append(ind2)
    else:
      nodetable.append(t[1])
      ldi2.append(nmax)
      nmax = nmax + 1
    ##結合
    n = ldi1[i]
    ncm[n] +=  1
    nd[n,ncm[n]-1] = i
    i += 1
  knl = i
  print("往復合計リンク数",knl)

orig = nodetable.index(onode)
dest = nodetable.index(dnode)

  ##ダイクストラ�? 0.005(s)
visited =[False] * nmax
arivetime = [max] * nmax
arivetime[orig] = 0
llink =[0] * nmax
lnode =[0] * nmax
nodename =[]
heapq.heappush(nodename,[0,orig]) 
while len(nodename) > 0:  ##ネック
  _,next = heapq.heappop(nodename)
  i = next
  visited[i] = True
  for k in range(ncm[i]):
    lk = int(nd[i,k])
    n = ldi2[lk]
    if(visited[n] == True):
      continue
    if((arivetime[i] + tt[lk]) < arivetime[n]):
      arivetime[n] = arivetime[i] + tt[lk]
      lnode[n] = i
      llink[n] = lk
      heapq.heappush(nodename, [arivetime[n],n])
print("旅行時間",arivetime[dest])

##最適経路探索 0.001s(while消したい)
keiro = [None] * 1500
nown = dest 
travel_l = 0
travel_dis = 0
while nown != orig:  ##リスト内でいけるかな
  travel_dis +=  length[llink[nown]]
  keiro[travel_l] = llink[nown]
  nown = lnode[nown]
  travel_l += 1

print("走行距離",travel_dis)
print("通過リンク数",travel_l)

##outputファイルに書き込み 0.001s(できたらnumpy)
f_out.writelines('node1,node2,dir,travel_time\n')
data = [(str([nodetable[ldi1[keiro[i]]], nodetable[ldi2[keiro[i]]], 0, tt[keiro[i]]]))
if nodetable[ldi1[keiro[i]]] < nodetable[ldi2[keiro[i]]]
else (str([nodetable[ldi2[keiro[i]]], nodetable[ldi1[keiro[i]]], 1, tt[keiro[i]]]))
for i in reversed(range(travel_l))] 
f_out.writelines(data)
f_out.close() 

 ##時間計測
end_time = time.perf_counter()

elapsed_time = end_time - start_time
print("CPU時間",elapsed_time)