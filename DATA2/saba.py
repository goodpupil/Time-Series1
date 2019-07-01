import numpy as np
import matplotlib.pyplot as plt
w=8 #weeks+1
a=np.zeros(w)
z=np.zeros(w)
m=np.zeros(w)
v=np.zeros(w)
d=(np.ones(w-1))*2
a[0]=10000
z[0]=0
m[0]=0
#parameters
alpha_p=0.305
beta_p=0.10892
alpha_h=0.305
beta_h=0.10892
t=7 #daily
tg=34.27*7
OER=1.7
ts=31.45*7
for i in range(w-1):
    print(i)
    m[i+1]=a[i]*(1-np.exp(-alpha_p*d[i]-beta_p*(d[i]**2)))
    a[i+1]=a[i]*(np.exp(-alpha_p*d[i]-beta_p*(d[i]**2)))*(np.exp(t/tg))+m[i]*(np.exp((-alpha_h*d[i]-beta_h*(d[i]**2))/OER))
    z[i+1]=a[i]*(1-(np.exp(-alpha_p*d[i]-beta_p*(d[i]**2))))*(np.exp(-t/ts))+m[i]*(1-np.exp((-alpha_h*d[i]-beta_h*(d[i]**2))/OER))*(np.exp(-t/ts))+z[i]*(np.exp(-t/ts))

    v[i+1]=m[i+1]+a[i+1]+z[i+1]
print(m)
print(a)
print(z)
fig=plt.figure()
plt.plot(m,"m").legend()
plt.plot(a,"a").legend()
plt.plot(z,"z").legend()
plt.show()
# print(v)


aaa=1