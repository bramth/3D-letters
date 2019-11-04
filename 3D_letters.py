# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:00:07 2019

@author: s1491784
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

# keymap reset

def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)

# ----------------- slicer -----------------

def multi_slice_viewer(volume):
    
    def process_key(event):
        fig = event.canvas.figure
        ax = fig.axes
        if event.key == '1':
            previous_slice(ax,0)
        elif event.key == '2':
            next_slice(ax,0)
        elif event.key == '3':
            previous_slice(ax,1)
        elif event.key == '4':
            next_slice(ax,1)
        elif event.key == '5':
            previous_slice(ax,2)
        elif event.key == '6':
            next_slice(ax,2)
                            
        fig.canvas.draw()
    
    def previous_slice(ax,idx):
        volume = ax[idx].volume
        if ax[idx].index > 0: 
            ax[idx].index = (ax[idx].index - 1)
            
            ax[idx].images[0].set_array(volume.swapaxes(0,idx)[ax[idx].index])
            ax[idx].set_title(ax[idx].index)
    
    def next_slice(ax,idx):
        volume = ax[idx].volume
        if ax[idx].index < volume.shape[0]-1: 
            ax[idx].index = (ax[idx].index + 1)
            ax[idx].images[0].set_array(volume.swapaxes(0,idx)[ax[idx].index])
            ax[idx].set_title(ax[idx].index)    
    
    remove_keymap_conflicts({'1', '2','3','4','5','6'})
    fig, axes = plt.subplots(1,3)
    
    for idx,ax in enumerate(axes):
        ax.volume = volume
        ax.index = volume.shape[idx] // 2
        im = ax.imshow(volume.swapaxes(0,idx)[ax.index,:,:])
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        
    fig.colorbar(im, ax=axes,shrink=0.3)
    fig.canvas.mpl_connect('key_press_event', process_key)


#def multi_slice_viewer(volume):
#    remove_keymap_conflicts({'a', 'd'})
#    fig, ax = plt.subplots()
#    ax.volume = volume
#    ax.index = volume.shape[0] // 2
#    ax.imshow(volume[ax.index])
#    fig.canvas.mpl_connect('key_press_event', process_key)
#
#def process_key(event):
#    fig = event.canvas.figure
#    ax = fig.axes[0]
#    if event.key == 'a':
#        previous_slice(ax)
#    elif event.key == 'd':
#        next_slice(ax)
#    fig.canvas.draw()
#
#def previous_slice(ax):
#    volume = ax.volume
#    if ax.index > 0: 
#        ax.index = (ax.index - 1)
#        ax.images[0].set_array(volume[ax.index])
#        ax.set_title(ax.index)
#
#def next_slice(ax):
#    volume = ax.volume
#    if ax.index < volume.shape[0]-1: 
#        ax.index = (ax.index + 1)
#        ax.images[0].set_array(volume[ax.index])
#        ax.set_title(ax.index)          
 

# datetime function

def get_cur_datetime():
    """
    Function that return current date and time in string format.
    """
    from datetime import datetime
    return str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))


def folder_existence(mydir):
    """
    Check if folder of current date exists.
    If not, it creates one.
    """

    if not os.path.exists(mydir):
        print('Folder "{}" created.'.format(mydir))
        os.makedirs(mydir)

    return

# ----------------- rotate -----------------

def random_rotate3D(img3d,
                    plot = False):
    from scipy.ndimage.interpolation import rotate
    import random
    
    plane  = np.array(random.sample([0,1,2],2))
    deg    = np.array(random.uniform(0,360))
    
    img3d_rot = rotate(img3d,deg,plane,reshape=False) 
    
    if plot:
        multi_slice_viewer(img3d_rot)
        
    return img3d_rot

# ----------------- generate -----------------    

def generate_letter(letter='Q',
                    size=140,
                    padsize=50,
                    plot = True):
    shape = (size,size)
    letter_size = size

    # make a blank image for the text, initialized to transparent text color
    img = Image.new('L', shape,0)

    # get a font
    font = ImageFont.truetype("arial.ttf", letter_size)
    # get a drawing context
    d = ImageDraw.Draw(img)

    # draw text, full opacity
    d.text((size/20,-size/10), letter, font=font, fill=255)
    
#    img = img.rotate(90)
    
    img_array = np.array(img)
    
    img3d = np.zeros([size,size,size])
    idx = [round(size/2) - round(size/20),
           round(size/2) + round(size/20)]
    
    img3d[idx[0]:idx[1]] = img_array
    
    img3d = np.pad(img3d,padsize,'constant')   
    
    if plot:
        multi_slice_viewer(img3d)
    
    return img3d

if __name__ == '__main__':
    size = 140
    padsize = 50
    totsize = size + 2*padsize
    chars = ['A','X','M','W']
    letters = np.zeros([len(chars),totsize,totsize,totsize])
    
    
    for idx, char in enumerate(chars) :
        let = generate_letter(char)
        letters[idx] = random_rotate3D(let)
        
    folder_existence('results')
    np.save('results//3D_letters_' + get_cur_datetime() + '.npy',letters)
        
    


