#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:04:44 2019

@author: griggles
"""
import numpy as np
import pandas as pd

#used to access images in zip folder
from zipfile import ZipFile
from io import BytesIO

from PIL import Image
from IPython.display import display

#metrics
def squared_euclidean(x, y):
    return np.sum(np.square(x-y))
#____
    
    
    
class Recommender():
    
    
    #df should have columns vector and img_path, and should be indexed
    #by CID!
    def __init__(self, df_feature, df_meta, zip_path='data/images.zip', verbose=False, metric='squared_euclidean'):
        self.df_feature = df_feature
        self.df_meta = df_meta
        self.df_img_path = df_meta['img_path']
        self.verbose = verbose
        
        self.archive = ZipFile(zip_path, 'r')
        
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
    def _get_closest_k(self, k, cid_tgt, vectors):
        top_k = []
        count = 0
       # vectors = self.df_feature
        vector_tgt = vectors.loc[cid_tgt]
        for index, vector in vectors.iterrows():
            count += 1
            vector_dist = self.metric(vector_tgt.values, vector.values)
            self._keep_top_k(k, top_k, (vector_dist, index))
        
            if(self.verbose):
                print(count)
                print(top_k)
        
        return list(map(lambda x : x[1], top_k))
    
    def get_img(self, cid):
        img_data = self.archive.read('images/' + self.df_img_path[cid])
        return Image.open(BytesIO(img_data))
    
    def display_shoe(self, cid):
        display(self.get_img(cid))
            
    #recommend k similar shoes as cid
    def recommend_k(self, k, cid):
        #Hack, since it will return top recommendation as the cid itself!
        k += 1
        
        #filter on gender and shoe category before recommending
        
        df_meta_gender = self.df_meta[self.df_meta['Gender'] == self.df_meta.loc[cid]['Gender']]
        df_meta_gender_cat = df_meta_gender[df_meta_gender['Category'] == df_meta_gender.loc[cid]['Category']]
        
        df_filtered = df_meta_gender_cat[df_meta_gender_cat['SubCategory'] == df_meta_gender_cat.loc[cid]['SubCategory']]

        indices = df_filtered.index.values
        
        filtered = self.df_feature.loc[indices]
        
        top_k = self._get_closest_k(k, cid, filtered)
        
        return {'tgt': top_k[0], 'recommended': top_k[1:]}
        
    def display_k_recommendations(self, k, cid, display_target=True):
        recommendations = self.recommend_k(k, cid)['recommended']
                
        if display_target:
            print('target:')
            self.display_shoe(cid)
            print('')
        
        print('recommendations:')
        for cid_rec in recommendations:
            self.display_shoe(cid_rec)
            
            
        
            
        
        
        
        
    
    
    
        
        
    
