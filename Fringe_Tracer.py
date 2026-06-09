"""
Created on Mon 01 Jun 2026 16:30:00

@author: trmundy
"""

from PIL import Image, ImageFilter
from skimage.morphology import skeletonize
import numpy as np
import scipy as sp
import tkinter as tk
from tkinter import filedialog, simpledialog, Tk, ttk

# Returns a 2D array of local maxima
def processor(inp,pic,flt,prm,lvl,buul,rad):
    for i in range(len(pic)):
        if buul:
            ln1 = sp.signal.savgol_filter(pic[i],flt,2)
        else:
            ln1 = pic[i]
        lnx = sp.signal.find_peaks(ln1,prominence=prm)[0]
        for j in range(len(lnx)):
            tj = lnx[j]
            inp[i][tj] = lvl
            m = i+rad
            n = tj+rad
            while m>=len(pic):
                m = m-1
            while n>=len(ln1):
                n = n-1
            while m>=i-rad and m>=0:
                while n>=tj-rad and n>=0:
                    inp[m][n] += lvl
                    n = n-1
                m = m-1
    p.step(2)
    win.update()
    return inp

# Creates a heat map of fringe locations based on overlapping locations of
# local maxima using different levels of filtering
def multiproc(inp,img):
    inp = processor(inp,img,0,0,15,False,1)
    inp = processor(inp,img,7,10,25,True,1)
    inp = processor(inp,img,11,30,37,True,2)
    inp = processor(inp,img,17,60,25,True,2)
    inp = processor(inp,img,23,100,25,True,3)
    return inp

# Gotta have a progress bar...
win = Tk()
win.geometry("750x250")
win.title("Image Processing Progress")
p = ttk.Progressbar(win,length=700)
p.place(x=25,y=125)

imgfl = filedialog.askopenfilename(title="Select Image:")

img = Image.open(imgfl)
img = np.array(img)
img = img-np.min(img)
img = (255*(img/np.max(img))).astype(np.uint8)
img = Image.fromarray(img)

img_med = img.filter(ImageFilter.MedianFilter(size=3))
img_med = np.array(img_med)

img_med_inv = 255-img_med

dark_fringes = np.zeros_like(img_med_inv).astype(float)
light_fringes = np.zeros_like(img_med).astype(float)
p.step(0.5)
win.update()
dark_fringes = multiproc(dark_fringes,img_med_inv)
light_fringes = multiproc(light_fringes,img_med)
img_med_inv = img_med_inv.T
dark_fringes = dark_fringes.T
img_med = img_med.T
light_fringes = light_fringes.T
dark_fringes = multiproc(dark_fringes,img_med_inv)
light_fringes = multiproc(light_fringes,img_med)

img_gauss = img.filter(ImageFilter.GaussianBlur(radius=3))
img_gauss = np.array(img_gauss)
img_gauss_inv = 255-img_gauss

dark_fringes = dark_fringes.T
light_fringes = light_fringes.T

dark_fringes = multiproc(dark_fringes,img_gauss_inv)
light_fringes = multiproc(light_fringes,img_gauss)
img_gauss_inv = img_gauss_inv.T
dark_fringes = dark_fringes.T
img_gauss = img_gauss.T
light_fringes = light_fringes.T
dark_fringes = multiproc(dark_fringes,img_gauss_inv)
light_fringes = multiproc(light_fringes,img_gauss)

dark_fringes = dark_fringes-np.min(dark_fringes)
dark_fringes = ((dark_fringes/np.max(dark_fringes))*255).astype(np.uint8)

light_fringes = light_fringes-np.min(light_fringes)
light_fringes = ((light_fringes/np.max(light_fringes))*255).astype(np.uint8)

dark_fringe_img = Image.fromarray(dark_fringes)
dark_fringe_img = dark_fringe_img.filter(ImageFilter.MedianFilter(size=3))
dark_fringe_img = dark_fringe_img.filter(ImageFilter.GaussianBlur(radius=5))
p.step(0.5)
win.update()
light_fringe_img = Image.fromarray(light_fringes)
light_fringe_img = light_fringe_img.filter(ImageFilter.MedianFilter(size=3))
light_fringe_img = light_fringe_img.filter(ImageFilter.GaussianBlur(radius=5))
p.step(0.5)
win.update()

dark_fringes= np.array(dark_fringe_img).astype(float)
light_fringes = np.array(light_fringe_img).astype(float)

output = dark_fringes-light_fringes
tip = int(len(output)/8)
for i in range(len(output)):
    for j in range(len(output[0])):
        if output[i][j]<0:
            output[i][j]=0
    if i%tip == 0:
        p.step(1.0)
        win.update()
        
output = ((output/np.max(output))*255).astype(np.uint8)
output_img = Image.fromarray(output)
output_img = output_img.filter(ImageFilter.MedianFilter(size=5))
output = np.array(output_img)
p.step(0.49)
win.update()

output_binary = np.zeros_like(output)
thrs = 20
for i in range(len(output)):
    for j in range(len(output[0])):
        if output[i][j] > thrs:
            output_binary[i][j] = 1
    if i%tip == 0:
        p.step(1.0)
        win.update()

fringe_traces_bin = skeletonize(output_binary)

fringe_traces = fringe_traces_bin.astype(np.uint8)
fringe_traces = 1-fringe_traces
fringe_traces = (255*fringe_traces).astype(np.uint8)
fringe_traces_img = Image.fromarray(fringe_traces.T)

fringe_traces_img.show()

flsv = tk.messagebox.askyesno(title="Save File?", message="Save Image?")
if flsv:
    flsn = filedialog.asksaveasfilename(title="Save As")
    flext = simpledialog.askstring(title="Save as type", prompt="File type to save image as:")
    fringe_traces_img.save(flsn,flext,compress_level=0)

win.destroy()
