import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np


import skimage.data
from sklearn.datasets import fetch_lfw_people
from skimage import data, transform, color, feature
from sklearn.feature_extraction.image import PatchExtractor
from itertools import chain
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV

imgs_to_use = ['camera', 'text', 'coins', 'moon',
               'page', 'clock', 'immunohistochemistry',
               'chelsea', 'coffee', 'hubble_deep_field']

def extract_patches(img, N, scale=1.0, patch_size=positive_patches[0].shape):
    
  extracted_patch_size = tuple((scale * np.array(patch_size)).astype(int))
  extractor = PatchExtractor(patch_size=extracted_patch_size,max_patches=N, random_state=0)
  patches = extractor.transform(img[np.newaxis])
  if scale != 1:
      patches = np.array([transform.resize(patch, patch_size) for patch in patches])
  
  return patches

def train():
  
    faces = fetch_lfw_people()
    positive_patches = faces.images
    positive_shape = positive_patches.shape
    
    images = [color.rgb2gray(getattr(data, name)()) for name in imgs_to_use]
    
    negative_patches = np.vstack([extract_patches(im, 1000, scale)
    
    for im in images for scale in [0.5, 1.0, 2.0]])
        print negative_patches.shape
        
    X_train = np.array([feature.hog(im) for im in chain(positive_patches, negative_patches)])
    y_train = np.zeros(X_train.shape[0])
    y_train[:positive_patches.shape[0]] = 1
    
    
    grid = GridSearchCV(LinearSVC(), {'C': [1.0, 2.0, 4.0, 8.0]})
    grid.fit(X_train, y_train)
    grid.best_score_
    
    model = grid.best_estimator_
    
    print "going into Training Step"
    model.fit(X_train, y_train)
    
    return model


def return_resized(img_path,height,width,save_location=None):
	img = cv2.imread(img_path,0)
	img = cv2.resize(img,(width,height))
	if save_location:
		name,extension = img_path.split('.')
        cv2.imwrite(name+"_resized"+extension,img) 
	else:
	    return img

def return_flattened_np(cv2_img_obj):
	np_img = np.asarrray(cv2_img_obj)
	return np_img.flatten()


