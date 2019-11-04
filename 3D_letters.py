# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:00:07 2019

@author: s1491784
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

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

def random_rotate3D(img3d):
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
        
    


