# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:24:43 2016
This module contains some useful digital filter for signal processing.
@author: Xmon-SC05
"""
from numpy import cos, sin, pi, absolute, arange, trapz,ones
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
from numpy.fft import fft,rfft,rfftfreq
from time import time

def savitzky_golay(y, window_size, order, deriv=0, rate=1):

    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
#    except ValueError, msg:
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
    
def lowpass_filter(x,fc,samplerate,trans_width=10,ripple_db = 60.0):
    # The Nyquist rate of the signal.
    nyq_rate = samplerate / 2.0
    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate.
    width = trans_width/nyq_rate
    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)
    taps = firwin(N, fc/nyq_rate, window=('kaiser', beta))
    
    figure()
#    clf()
    w, h = freqz(taps, worN=8000)
    plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
    xlabel('Frequency (Hz)')
    ylabel('Gain')
    title('Frequency Response')
    ylim(-0.05, 1.05)
    grid(True)
    
    delay = 0.5 * (N-1) / samplerate
    return lfilter(taps, 1.0, x),delay
    
if __name__ == '__main__':
#------------------------------------------------
# Create a signal for demonstration.
#------------------------------------------------

    sample_rate = 100.0
    nsamples = 400
    t = arange(nsamples) / sample_rate
    x = cos(2*pi*0.5*t) + 0.2*sin(2*pi*2.5*t+0.1) + \
        0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + \
            0.1*sin(2*pi*23.45*t+.8)  
            
    filtered_x,delay=lowpass_filter(x,10,sample_rate,5)
    
    figure(),plot(t,x)
    plot(t-delay,filtered_x)
    
    sample_rate= 1e9
    nsamples = 1000
    t = arange(nsamples) / sample_rate
    f1,f2,f3=12e6,23e6,34e6
    x=0.3*cos(2*pi*f1*t)+0.8*cos(2*pi*f2*t+0.3*pi)+0.1*cos(2*pi*f3*t+0.8)
    x1=x.reshape((x.shape[-1],-1))*ones([1,3])
    
    ti=time()
    ref_1,ref_2,ref_3=cos(2*pi*f1*t),cos(2*pi*f2*t),cos(2*pi*f3*t)
    s1,s2,s3=trapz(x*ref_1),trapz(x*ref_2),trapz(x*ref_3)
    tf=time()
    print(tf-ti)
    
    filtered_x1,delay1=lowpass_filter(x*ref_1,1e6,sample_rate,20e6,40)
    
    ti=time()
    sp=rfft(x1,axis=0)
    freq = rfftfreq(t.shape[-1])
    tf=time()
    print(tf-ti)
    
    
    
    
    
    
    
    