# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 16:20:19 2024

@author: peter j. wlasits, florian wieland

Sensirion SEN55-Livegraph - A script to test the live-graphs on any pc no i2c and sen55 necessary as it
uses random values.
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator, AutoDateFormatter

import pandas as pd
import numpy as np

import datetime as dt
from datetime import datetime, timedelta
import random

#from sensirion_i2c_driver import I2cConnection, LinuxI2cTransceiver
#from sensirion_i2c_sen5x import Sen5xI2cDevice

#import board
#import time

matplotlib.use("TkAgg")

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

#with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:
#    device = Sen5xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-1')))
#    device.device_reset()
#    device.start_measurement()
        

# This function is called periodically from FuncAnimation
def animate(i, xs1, ys1, xs2, ys2, xs3, ys3, xs4, ys4, li, a, b, c, d, keep_interval):
    # Update sensor data
    #while device.read_data_ready() is False:
    #    time.sleep(0.1)

    #values = device.read_measured_values()

    #pm25 = values.mass_concentration_2p5.physical
    #RH_c = values.ambient_humidity.percent_rh
    #temp_c = values.ambient_temperature.degrees_celsius
    #VOC = values.voc_index.scaled
    #liney = 100
    #al = 60
    #bl = 35
    #cl = 0
    #dl = 10

    # Or use random numbers
    pm25 = random.randrange(0, 100, 3)
    RH_c = random.randrange(10, 60, 3)
    temp_c = random.randrange(0, 100, 3)
    VOC = random.randrange(10, 500, 3)

    # Update x and y lists
    now = dt.datetime.now()
    xs1.append(now)
    ys1.append(temp_c)
    xs2.append(now)
    ys2.append(RH_c)
    xs3.append(now)
    ys3.append(VOC)
    xs4.append(now)
    ys4.append(pm25)

    # Keep only the last keep_interval on plot
    xs1 = [x for x in xs1 if (now - x).seconds <= keep_interval]
    ys1 = ys1[-len(xs1):]
    xs2 = [x for x in xs2 if (now - x).seconds <= keep_interval]
    ys2 = ys2[-len(xs2):]
    xs3 = [x for x in xs3 if (now - x).seconds <= keep_interval]
    ys3 = ys3[-len(xs3):]
    xs4 = [x for x in xs4 if (now - x).seconds <= keep_interval]
    ys4 = ys4[-len(xs4):]

    # Clear axis and plot
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax1.plot(xs1, ys1, linewidth=2, color='firebrick')
    ax2.plot(xs2, ys2, linewidth=2, color='darkblue')
    ax3.plot(xs3, ys3, linewidth=2, color='darkgreen')
    ax4.plot(xs4, ys4, linewidth=2, color='darkorange')

    # Set xticks and format
    ax3.xaxis.set_major_locator(AutoDateLocator())
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax4.xaxis.set_major_locator(AutoDateLocator())
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # Format rotation
    for ax in [ax3, ax4]:
        ax.tick_params(axis='x', labelrotation=45)

    fig.tight_layout()

keep_interval = 600 # Time in seconds that are displayed in plot
ani = animation.FuncAnimation(fig, animate, fargs=(xs1, ys1, xs2, ys2, xs3, ys3, xs4, ys4, li, a, b, c, d, keep_interval),
                              interval=1000)
plt.show()
