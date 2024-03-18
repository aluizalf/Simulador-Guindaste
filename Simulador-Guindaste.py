from cmath import pi
import math as math
import numpy as np
from vpython import *
import plotly.offline as py
import plotly.graph_objs as go

#Dimensões das seções
espessura = []
altura = []
raio = []
i=1
aux=0
for k in range (3):
  while (i <= 3):
    print("---- Parâmetros da seção " + str(i) + " ----")
    e=float(input("Espessura da seção " + str(i) + ": "))
    espessura.append(e)
    h=float(input("Altura da seção " + str(i) + ": "))
    altura.append(h)
    r=float(input("Raio da seção " + str(i) + ": "))
    raio.append(r)
    i = i + 1

xbarra = []
ybarra = []
area = []
for k in range (3):
  e = espessura[k]
  h = altura[k]
  r = raio[k]
  #Centróide x e y (assumindo que todas as seções estão alinhadas ao centro do semicírculo)
  a1=h*e
  a2=h*e
  a3=(2*r-2*e)*e
  a4=((math.pi*(r**2)-math.pi*(r-e)**2)*0.5)
  xt1=(r-(e/2))
  xt2=(-r+(e/2))
  xt3=(0)
  xt4=(0)
  yt1=(h/2)
  yt2=(h/2)
  yt3=(h-(e/2))
  ayt4=((2*-r**3/3)-(2*-(r-e)**3/3))
  xb=((xt1*a1+xt2*a2+xt3*a3+xt4*a4)/(a1+a2+a3+a4))
  xbarra.append(xb)
  yb=((yt1*a1+yt2*a2+yt3*a3+ayt4)/(a1+a2+a3+a4))
  ybarra.append(yb)
  a = (a1+a2+a3+a4)
  area.append(a)

#Em z (variável):
l = float(input("Comprimento das lanças em m: "))
d = float(input("Densidade do material das lanças em kg/m^3: "))
g = float(input("Aceleração da gravidade em m/s^2: "))
xcl = float(input("Deslocamento linear das lanças em m: "))
grau = float(input("Ângulo em grau: "))
theta = math.radians(grau)
v1 = area[0]*l
v2 = area[1]*l
v3 = area[2]*l
w1 = (d*v1*g)
w2 = (d*v2*g)
w3 = (d*v3*g)
w = (w1 + w2 + w3) #peso total das lanças
z1 = z2 = z3 = (l/2) #xcl=0 e posiciona-se o eixo no ponto O

#Centro de gravidade x e y
xg = ((xbarra[0]*w1 + xbarra[1]*w2 + xbarra[2]*w3)/w)
yg = ((ybarra[0]*w1 + ybarra[1]*w2 + ybarra[2]*w3)/w)

#Estudo do cg da lança menor se deslocando [0<=xcl<=l]
if (0<=xcl and xcl<=l):
  zg3 = ((w3*(z3 + xcl)*math.cos(theta))/w)
  zg2 = ((w2*(z2*math.cos(theta)))/w)
  zg1 = ((w1*(z1*math.cos(theta)))/w)
  zg = (zg1 + zg2 + zg3)
  yg = (((ybarra[0] + z1*math.sin(theta))*w1 + (ybarra[1] + z2*math.sin(theta))*w2 + (ybarra[2] + (z3 + xcl)*math.sin(theta))*w3)/w)
  xg = ((xbarra[0]*w1 + xbarra[1]*w2 + xbarra[2]*w3)/w)

#Estudo do cg da lança intermediária se deslocando [l<=xcl<=2l]
if (l<=xcl and xcl<=(2*l)):
  zg3 = ((w3*(z3 + xcl)*math.cos(theta))/w)
  zg2 = (w2*(z2 + xcl - l)*math.cos(theta)/w)
  zg1 = (w1*(z1*math.cos(theta))/w)
  zg = (zg1 + zg2 + zg3)
  yg = (((ybarra[0] + z1*math.sin(theta))*w1 + (ybarra[1] + (z2 + xcl - l)*math.sin(theta))*w2 + (ybarra[2] + (z3 + xcl)*math.sin(theta))*w3)/w)
  xg = ((xbarra[0]*w1 + xbarra[1]*w2 + xbarra[2]*w3)/w)

#Força máxima
D1= float(input("Forneça o tamanho da base em metros: "))

Dcox= (l + xcl)*math.cos(theta)

Xf = Dcox - D1/2
Xcg= zg - D1/2
Pcg= w

F= (Pcg*Xcg)/Xf

#----Animação----
#Cena
scene.width = 600
scene.height = 450
scene.title = "GUINDASTE DASTE"
scene.center = vec(1.3*l,0.6*l,0)
scene.range = 2*l

#Base
rotula1=sphere(pos=vector(0,0,0), radius=1.8, color=color.yellow)
cone=cone(pos=vector(-3.6,0,0), axis=vector(4,0,0), radius=1.8)
cone.rotate(angle=pi/2, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
base=box(pos=vector(3.4,-4.6,0),length=10, height=3, width=10)
eixox = arrow(pos=vector(0,0,1), axis=vector(0,0,4), shaftwidth=0.5, color=color.red, headwidth=0.75)
nex=label(pos=eixox.pos,text='x', xoffset=-5, yoffset=-5, space=30, height=16, border=4, font='sans', opacity=0, box=False, color=color.white, line=False)
eixoy = arrow(pos=vector(0,1,0), axis=vector(0,4,0), shaftwidth=0.5, color=color.blue, headwidth=0.75)
ney=label(pos=eixoy.pos,text='y', xoffset=0, yoffset=20, space=30, height=16, border=4, font='sans', opacity=0, box=False, color=color.white, line=False)
eixoz = arrow(pos=vector(1,0,0), axis=vector(4,0,0), shaftwidth=0.5, color=color.green, headwidth=0.75)
nez=label(pos=eixoz.pos,text='z', xoffset=20, yoffset=0, space=30, height=16, border=4, font='sans', opacity=0, box=False, color=color.white, line=False)

#Incrementos
deltat = 0.005
t = 0
rot = 0
alt=-5
larg=-(l+xcl)


#Movimento da lança
c1=cylinder(pos=vector(0,0,0), radius=1.5, axis=vector(l,0,0), color=color.white, opacity=0.3)

if (0<=xcl and xcl<=l):
  c3 = cylinder(pos=vector(l, 0, 0), radius=1.1, color=color.white, opacity=0.3)
  ball = sphere(radius=0.75, color=color.red, origin=vector(0, 0, 0), make_trail=True)
  while t < xcl:
    c3.axis=vector(t, 0, 0)
    rate(100)
    t = t + deltat
    zg3 = ((w3*(z3 + t)*math.cos(0))/w)
    zg2 = ((w2*(z2*math.cos(0)))/w)
    zg1 = ((w1*(z1*math.cos(0)))/w)
    zg = (zg1 + zg2 + zg3)
    yg = (((ybarra[0] + z1*math.sin(0))*w1 + (ybarra[1] + z2*math.sin(0))*w2 + (ybarra[2] + (z3 + xcl)*math.sin(0))*w3)/w)
    xg = ((xbarra[0]*w1 + xbarra[1]*w2 + xbarra[2]*w3)/w)
    ball.pos.x = zg

  cabo = cylinder(pos=vector(alt, larg, 0), radius=0.05, axis=vector(5, 0, 0), color=color.white, opacity=1)
  cabo.rotate(angle=pi / 2, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
  carga = box(pos=cabo.pos, length=3, height=3, width=3, color=color.magenta)
  while (rot <= theta) and (theta != 0):
    rate(5)
    c1.rotate(angle=0.0174533, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
    c3.rotate(angle=0.0174533, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
    rot = rot + 0.0174533
    zg3 = ((w3*(z3 + t)*math.cos(rot))/w)
    zg2 = ((w2*(z2*math.cos(rot)))/w)
    zg1 = ((w1*(z1*math.cos(rot)))/w)
    zg = (zg1 + zg2 + zg3)
    yg = (((ybarra[0] + z1*math.sin(rot))*w1 + (ybarra[1] + z2*math.sin(rot))*w2 + (ybarra[2] + (z3 + xcl)*math.sin(rot))*w3)/w)
    xg = ((xbarra[0]*w1 + xbarra[1]*w2 + xbarra[2]*w3)/w)
    ball.pos = vector(zg,yg,0)
    tx = larg * sin(rot) + 5
    ty = -larg * cos(rot)
    cabo.pos = vector(ty, -tx, 0)
    carga.pos = cabo.pos

if (l<xcl and xcl<=(2*l)):
  c3 = cylinder(pos=vector(l, 0, 0), radius=1.1, color=color.white, opacity=0.3)
  ball = sphere(radius=0.75, color=color.red, origin=vector(0, 0, 0), make_trail=True)
  while t < l:
    rate(100)
    c3.axis=vector(t, 0, 0)
    t = t + deltat
    zg3 = ((w3 * (z3 + t) * math.cos(0)) / w)
    zg2 = ((w2 * (z2 * math.cos(0))) / w)
    zg1 = ((w1 * (z1 * math.cos(0))) / w)
    zg = (zg1 + zg2 + zg3)
    yg = (((ybarra[0] + z1 * math.sin(0)) * w1 + (ybarra[1] + z2 * math.sin(0)) * w2 + (ybarra[2] + (z3 + xcl) * math.sin(0)) * w3) / w)
    xg = ((xbarra[0] * w1 + xbarra[1] * w2 + xbarra[2] * w3) / w)
    ball.pos.x = zg
    q = zg
  t = 0
  c2 = cylinder(pos=vector(l, 0, 0), radius=1.3, color=color.white, opacity=0.3)
  while t < (xcl-l):
    rate(100)
    ball.pos.x = zg
    c3.pos.x=c2.pos.x+t
    c2.axis=vector(t, 0, 0)
    t = t + deltat
    zg3 = ((w3 * (z3 + l + t) * math.cos(0)) / w)
    zg2 = (w2 * (z2 + t) * math.cos(0) / w)
    zg1 = (w1 * (z1 * math.cos(0)) / w)
    zg = (zg1 + zg2 + zg3)
    yg = (((ybarra[0] + z1 * math.sin(0)) * w1 + (ybarra[1] + (z2 + t) * math.sin(0)) * w2 + (ybarra[2] + (z3 + xcl) * math.sin(0)) * w3) / w)
    xg = ((xbarra[0] * w1 + xbarra[1] * w2 + xbarra[2] * w3) / w)
    ball.pos.x = zg
  cabo = cylinder(pos=vector(alt, larg, 0), radius=0.05, axis=vector(5, 0, 0), color=color.white, opacity=1)
  cabo.rotate(angle=pi / 2, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
  carga = box(pos=cabo.pos, length=3, height=3, width=3, color=color.magenta)
  while (rot <= theta) and (theta != 0):
    rate(5)
    c1.rotate(angle=0.0174533, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
    c2.rotate(angle=0.0174533, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
    c3.rotate(angle=0.0174533, origin=vector(0, 0, 0), axis=vector(0, 0, 1))
    rot = rot + 0.0174533
    zg3 = ((w3 * (z3 + xcl) * math.cos(rot)) / w)
    zg2 = (w2 * (z2 + t) * math.cos(rot) / w)
    zg1 = (w1 * (z1 * math.cos(rot)) / w)
    zg = (zg1 + zg2 + zg3)
    yg = (((ybarra[0] + z1 * math.sin(rot)) * w1 + (ybarra[1] + (z2 + t) * math.sin(rot)) * w2 + (ybarra[2] + (z3 + xcl) * math.sin(rot)) * w3) / w)
    xg = ((xbarra[0] * w1 + xbarra[1] * w2 + xbarra[2] * w3) / w)
    ball.pos = vector(zg, yg, 0)
    tx = larg * sin(rot) + 5
    ty = -larg * cos(rot)
    cabo.pos = vector(ty, -tx, 0)
    carga.pos = cabo.pos

#Dados de saída
ball=sphere(pos=vector(zg,yg,0), radius=0.75, color=color.red, origin=vector(0,0,0))
nbola=label(pos=ball.pos,text='cg', xoffset=0, yoffset=10, space=30, height=10, border=4, font='sans', opacity=0, box=False, color=color.white)
massa=label(pos=carga.pos,text=(round(F/g,3),'kg'), xoffset=0, yoffset=0, space=30, height=16, border=4, font='sans', opacity=0, box=False, color=color.white, line=False)

