#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:04:44 2019

@author: griggles
"""
import numpy as np
import pandas as pd
from PIL import Image
from IPython.display import display 


#metrics
def squared_euclidean(x, y):
    return np.sum(np.square(x-y))
#____
    
    
    
class Recommender():
    
    
    #df should have columns vector and img_path, and should be indexed
    #by CID!
    def __init__(self, df_feature, df_img_path, verbose=False, metric='squared_euclidean'):
        self.df_feature = df_feature
        self.df_img_path = df_img_path
        self.verbose = verbose
        
        if metric == 'squared_euclidean':
            self.metric = squared_euclidean
    
    def _keep_top_k(self, k, top_k, challenger):
        if len(top_k) < k:
            top_k.append(challenger)
            top_k = sorted(top_k)
            return top_k
    
        insert_index = -1
        
        for i in range(k - 1, -1, -1):
            if top_k[i][0] > challenger[0]:
                insert_index = i
            else:
                break
            
        if insert_index >= 0:
            top_k.insert(insert_index, challenger)
        if len(top_k) > k:
            top_k = top_k.pop()
            
        return top_k
    
    
    #metric is a distance metric x, y -> R
    def _get_closest_k(self, k, cid_tgt):
        top_k = []
        count = 0
        vectors = self.df_feature
        vector_tgt = vectors.loc[cid_tgt]
        for index, vector in vectors.iterrows():
            count += 1
            vector_dist = self.metric(vector_tgt.values, vector.values)
            self._keep_top_k(k, top_k, (vector_dist, index))
        
            if(self.verbose):
                print(count)
                print(top_k)
        
        return list(map(lambda x : x[1], top_k))
    
    
    #display recommendations
    def display_recs(self, cid_tgt, cids):
        img_paths = self.df_img_path
        img_tgt = Image.open(img_paths[cid_tgt])
        img_list = [img_tgt]
        
        for cid in cids:
            img_list.append(Image.open(img_paths[cid]))
            
        for img in img_list:
            display(img)
            
    def display_target(self, cid_tgt):
        img_paths = self.df_img_path
        img_tgt = Image.open(img_paths[cid_tgt])
        display(img_tgt)
            
    #recommend k similar shoes as cid
    def recommend_k(self, k, cid):
        top_k = self._get_closest_k(k, cid)
        self.display_recs(top_k[0], top_k[1:])
        
        
        
    
    
    
        
        
    