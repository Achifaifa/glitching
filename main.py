#! /usr/bin/env python

import copy, itertools, math, random
from skimage import io
import numpy as np

dbpic=io.imread("./ta.jpeg",as_grey=False)
dbpicbw=io.imread("./ta.jpeg",as_grey=True)

t=[[[k for k in j] for j in i] for i in dbpic]
tbw=[[j for j in i] for i in dbpicbw]
tot_h, tot_v = len(t[0]), len(t)

def separate_colours(img):

  r=[[j[0] for j in i] for i in t]
  g=[[j[1] for j in i] for i in t]
  b=[[j[2] for j in i] for i in t]

  return r,g,b

def join_colours(r,g,b):

  return [list(zip(r[i],g[i],b[i])) for i in range(tot_v)]


def bw_move_horiz(matrix, h_start, dh, v_start, dv, disp):
  """
  Moves a subsection of the image horizontally
  """

  dh=tot_h-h_start if h_start+dh>tot_h else dh
  dv=tot_v-v_start if v_start+dv>tot_v else dv
  disp=0 if abs(disp)+h_start+dh>tot_h else disp

  for i in range(dv):
    matrix[v_start+i]=matrix[v_start+i][:h_start]+\
                  matrix[v_start+i][h_start-disp:][:dh]+\
                  matrix[v_start+i][h_start+dh:]
    if len(matrix[v_start+i])<tot_h: 
      matrix[v_start+i]=matrix[v_start+i]+matrix[v_start+i-1]+matrix[v_start+i-2]+matrix[v_start+i-3]
    if len(matrix[v_start+i])>tot_h: matrix[v_start+i]=matrix[v_start+i][:tot_h]

def bw_move_vert(matrix, h_start, dh, v_start, dv, disp):
  """
  Moves a subsection of the image vertically
  """

  dh=tot_h-h_start if h_start+dh>tot_h else dh
  dv=tot_v-v_start if v_start+dv>tot_v else dv
  disp=0 if v_start+dv+abs(disp)>tot_v else disp

  rng=range(v_start+dv, v_start, -1) if disp>0 else range(v_start, v_start+dv, 1)

  for i in rng:
    matrix[i]=matrix[i][:h_start]+matrix[i-disp][h_start:h_start+dh]+matrix[i][h_start+dh:]

def bw_mess_colours(h_start, dh, v_start, dv, fuckup):
  """
  Screws up colour in a zone
  Fuckup goes from 0 (nothing) to 100 (maxi fuckup)
  Doesn't work 
  """

  for i in range(dv):
    if fuckup>0:
      t[v_start+i]=[j+random.randint(0,fuckup)/100 for j in t[v_start+i]]
      t[v_start+i]=[1 if j>1 else j for j in t[v_start+i]]
    if fuckup<0:
      t[v_start+i]=[j+(random.randint(fuckup, 0)/100) for j in t[v_start+i]]
      t[v_start+i]=[0 if j<0 else j for j in t[v_start+i]]

def serialize_image(matrix):
  
  return list(itertools.chain.from_iterable(matrix))

def deserialize_image(data):

  return [[j for j in i] for i in np.array_split(data, tot_v)]

def generatesections(num, len):

  sections=[]
  last=0
  for i in range(num):
    sections.append([])
    for i in range(2):
      sections[-1].append(random.randint(last,len))
      last=sections[-1][-1]

  return sections

def checksection(sections, number):

  for i in sections: 
    if i[1]>number>i[0] : return 1 
  return 0

def interference(dat, sections):

  noise_sections=generatesections(sections,len(dat))
  for i in range(len(dat)):
    dat[i]=random.random()*dat[i] if checksection(noise_sections,i) else dat[i]
  return dat
  
r,g,b=separate_colours(t)

for i in range(300):
  col=random.choice([r,g,b])
  if random.choice([0,1]):
    bw_move_horiz(col, random.randint(1,250), random.randint(100,230), random.randint(0,340), random.randint(0,20), random.randint(-30,30))
  else:
    bw_move_vert(col, random.randint(1,250), random.randint(1,23), random.randint(0,340), random.randint(150,300), random.randint(-30,30))
for i in range(3):
  bw_move_horiz(tbw, random.randint(1,250), random.randint(100,230), random.randint(0,340), random.randint(0,20), random.randint(-30,30))

# for i in range(3):
#   col=[r,g,b][i]
#   data=serialize_image(col)
#   data=interference(data,10)
#   data=[254 if i>254 else i for i in data]
#   col=deserialize_image(data)

print tot_h*tot_v 
data=serialize_image(r)
print len(data)
data=[data[i]*abs(math.sin(i*2*math.pi/100)) for i in range(len(data))]
r=deserialize_image(data)

# data=serialize_image(g)
# data=[data[i]*abs(math.sin((i+50)*2*math.pi/100)) for i in range(len(data))]
# g=deserialize_image(data)

# data=serialize_image(b)
# data=[data[i]*abs(math.sin((i+100)*2*math.pi/100)) for i in range(len(data))]
# b=deserialize_image(data)



t=join_colours(r,g,b)



t_out=np.array(t)
io.imshow(t_out)
io.show()