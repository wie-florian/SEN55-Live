# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 16:20:19 2024

@author: peter, florian wieland

Sensirion SEN55-Livegraph - A script to show live graphs of SEN55 data on a raspberry pi 4 via i2c.
"""


import datetime as dt
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator, AutoDateFormatter
from sensirion_i2c_driver import I2cConnection, LinuxI2cTransceiver
from sensirion_i2c_sen5x import Sen5xI2cDevice


# Create figure for plotting
fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2,sharex=True,sharey=False, figsize=(10,5))
#ax = fig.add_subplot(1, 1, 1)
xs1 = []
ys1 = []
xs2 = []
ys2 = []
xs3 = []
ys3 = []
xs4 = []
ys4 = []
li=[]
a=[]
b=[]
c=[]
d=[]

with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:
	device = Sen5xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-1')))         
	device.device_reset()
	device.start_measurement()
        

# This function is called periodically from FuncAnimation
def animate(i, xs1, ys1,xs2,ys2,xs3,ys3,xs4,ys4,li,a,b,c,d,keep_interval=600):
           
    while device.read_data_ready() is False:
            time.sleep(0.1)
        
    values = device.read_measured_values()
        
    pm25 =values.mass_concentration_2p5.physical
    RH_c = values.ambient_humidity.percent_rh
    temp_c =values.ambient_temperature.degrees_celsius
    VOC = values.voc_index.scaled
    liney=100
    al=60
    bl=35
    cl=0
    dl=10
    #print(str(temp_c))
#     
    # Add x and y to lists
    xs1.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys1.append(temp_c)
    
    xs2.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys2.append(RH_c)
    xs3.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys3.append(VOC)
    xs4.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys4.append(pm25)
    li.append(liney)
    a.append(al)
    b.append(bl)
    c.append(cl)
    d.append(dl)

    # Keep only the last keep_interval on plot
    xs1 = [x for x in xs1 if (now - x).seconds <= keep_interval]
    ys1 = ys1[-len(xs1):]
    xs2 = [x for x in xs2 if (now - x).seconds <= keep_interval]
    ys2 = ys2[-len(xs2):]
    xs3 = [x for x in xs3 if (now - x).seconds <= keep_interval]
    ys3 = ys3[-len(xs3):]
    xs4 = [x for x in xs4 if (now - x).seconds <= keep_interval]
    ys4 = ys4[-len(xs4):]
    
    li=li[-50:]
    a=a[-50:]
    b=b[-50:]
    c=c[-50:]
    d=d[-50:]

    # Draw x and y lists
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax1.plot(xs1, ys1,linewidth=2,color='firebrick')
    ax1.plot(xs1, b,linewidth=2,color='None')
    ax1.plot(xs1, d,linewidth=2,color='None')
    #ax1.scatter(xs1, ys1,color='firebrick')
    ax2.plot(xs2, ys2,linewidth=2,color='darkblue')
    ax2.plot(xs2, d,linewidth=2,color='None')
    ax2.plot(xs2, a,linewidth=2,color='None')
    #ax2.scatter(xs2, ys2,color='darkblue')
    ax3.plot(xs3, ys3,linewidth=2,color='darkgreen')
    ax3.plot(xs3, li,linewidth=2,color='darkgreen',linestyle='dashed')
    #ax3.scatter(xs3, ys3,color='darkgreen')
    ax4.plot(xs4, ys4,linewidth=2,color='darkorange')
    ax4.plot(xs4, c,linewidth=2,color='None')
    #ax4.scatter(xs4, ys4,color='darkorange')
    
    #print(str(pm25))
    
    # Format plot
    ax3.tick_params(axis='x',labelrotation=45)
    ax4.tick_params(axis='x',labelrotation=45)
    
    #ax3.set_xlabel('Time [hh:mm:ss]')#,fontsize=14)
    #ax4.set_xlabel('Time [hh:mm:ss]')#,fontsize=14)
    
    ax3.set_xlabel('Time')#,fontsize=14)
    ax4.set_xlabel('Time')#,fontsize=14)
    ax3.set_xticks([])
    ax4.set_xticks([])
    
    ax1.set_ylabel('Temperature [°C]',color='firebrick')#,fontsize=14)
    ax2.set_ylabel('Rel. Humidity [%]',color='darkblue')#,fontsize=14)
    ax3.set_ylabel('VOC Index []',color='darkgreen')#,fontsize=14)
    ax4.set_ylabel('PM2.5 [$\mu$g/m$^3$]',color='darkorange')#,fontsize=14)
    
    #ax1.text(.1,.1,'text',fontsize=15)
    
    fig.tight_layout()
    
    print('Time: ',dt.datetime.now().strftime('%H:%M:%S'))
    print('Temperature: ',temp_c,'°C')
    print('Rel. Humidity: ',RH_c,'%')
    print('PM2.5: ',pm25,'mug/m^3')
    print('VOC Index: ',VOC)
    print('-*-*-*-*-*-*-*-*-')

keep_interval = 10
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs1,ys1,xs2,ys2,xs3,ys3,xs4,ys4,li,a,b,c,d,keep_interval), interval=10000)
#plt.get_current_fig_manager().full_screen_toggle()
plt.show()
