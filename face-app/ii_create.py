from PIL import Image , ImageDraw
import sys
import numpy as np
from skimage import data, color, feature
import skimage.data
from skimage.feature import hog

def return_ii(np_image):
    '''returns an integral image as np array'''
    rows = np_image.shape[0]
    columns = np_image.shape[1]
    for i in range(columns-1):
        np_image[0][i+1] += np_image[0][i]

    for j in range(rows-1):
        np_image[j+1][0] += np_image[j][0]
    
    for row_iter in range(rows-1):
        for column_iter in range(columns-1):
            np_image[row_iter+1][column_iter+1] += (np_image[row_iter+1][column_iter] +  np_image[row_iter][column_iter+1] -  np_image[row_iter][column_iter])
  
    return np_image


def area_sum_from_ii(ii,a,b,c,d):
    '''returns sum of area abcd from integral image (ii)'''
    rows = ii.shape[0]
    columns = ii.shape[1]
    
    sum = ii[a['x'],a['y']] + ii[d['x'],d['y']] - ii[b['x'],b['y']] - ii[c['x'],c['y']]

    return sum    



def traverse_window(img_arr,window_height,window_width):
    rows = img_arr.shape[0]
    columns = img_arr.shape[1]

    column_limit = columns - window_width + 1
    row_limit = rows - window_height + 1 
    
    draw = ImageDraw.Draw(img_arr)
    draw.rectangle(((0, 00), (100, 100)), fill="blue")
    
    for i in range(row_limit):
        for j in range(column_limit):
            pass



def hog_image(image="static/nm.jpg"):
    # image = color.rgb2gray(image)
    # hog_vec, hog_vis = feature.hog(image, visualise=True)
    # imshow(hog_vis)
    # return hog_vec
    image = data.astronaut()
    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1), visualize=True, multichannel=True)

            
        
    

if __name__ == '__main__':

    img = Image.open(sys.argv[1]).convert('L')
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 00), (24, 24)), outline="blue")
    img.show()
    img_as_np = np.asarray(img,dtype=np.uint64)
    #img_as_np = np.array([[1,1,1],[1,1,1],[1,1,1]])
    print img_as_np
    ii =  return_ii(img_as_np)
    print area_sum_from_ii(ii,{'x':0,'y':0},{'x':2,'y':0},{'x':0,'y':2},{'x':2,'y':2})
    

#/home/shubham/Desktop/FACEDATA/processed_nm3/modi_from_pdf.jpg


