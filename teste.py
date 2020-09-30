l=[[1, 3 , 6],[6,7,8], [], [4,4,4], []]
a=[]
h=[]

for i in l:
    if len(i)>0:
        a.append(i)
    else:
        a.append(None)
for e in a:
    if e != None:
        h.append(e)
print(h)
