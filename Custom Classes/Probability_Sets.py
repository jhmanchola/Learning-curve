#!/usr/bin/env python
# coding: utf-8

# In[50]:


import matplotlib.pyplot as plt

import numpy as np
import shapely.geometry as sg
from shapely.ops import cascaded_union,split
import shapely.affinity
import descartes

from itertools import combinations

import warnings


class Sets_Space():
    def __init__(self,name):
        
        self.name = name
        
        self.events = {}
        
        self.partitions = None
        
        self.additional_text = {}

        
    def add_Ellipse(self, name, loc, width, height, angle, res, fill_color, alpha,
                    text,fontsize, fontcolor, text_loc=None):
        
        from math import pi
        
        assert name not in self.events, "Name '%s'already saved. Choose another name."%name
        
        Area = (width)*(height)*pi
        
        Shape = shapely.affinity.scale(sg.Point(loc[0],loc[1]).buffer(1,res), width, height)
        
        if text_loc == None:
            text_loc = (Shape.centroid.x,Shape.centroid.y)
        else:
            text_loc = text_loc
        self.events[name] = dict(figure=shapely.affinity.rotate(
                                Shape,angle),
                                fill_color=fill_color, alpha=alpha, text=text, text_loc=text_loc,
                                fontsize=fontsize,fontcolor=fontcolor,area=Area)
    
   
    def add_Polygon(self, name, points, angle, fill_color, alpha, 
                    text, fontsize, fontcolor, text_loc=None):
                    
        assert name not in self.events, "Name '%s' already saved. Choose another name."%name            
        if points == None:          
            points = [(0.25,0.25),(0.5,0.75),(0.75,0.25)]
            Shape = sg.Polygon(points)
            warnings.warn("No points list given for Polygon, using default list: %s." % points)
                          
        else:
            Shape = sg.Polygon([(p[0],p[1]) for p in points])
        
        if text_loc == None:
            text_loc = (Shape.centroid.x,Shape.centroid.y)
        else:
            text_loc = text_loc
        
        Area = Shape.area
        
        
        self.events[name] = dict(figure=shapely.affinity.rotate(Shape,angle),
                                fill_color=fill_color, alpha=alpha, text=text, 
                                text_loc=text_loc,fontsize=fontsize,
                                fontcolor=fontcolor,area=Area)
        
        
    def add_Box(self, name, corners, angle, fill_color, alpha, 
                text, fontsize, fontcolor,text_loc=None):
            
        assert name not in self.events, "Name '%s' already saved. Choose another name."%name  
        
        if corners == None:          
            corners = [(0.25,0.25),(0.25,0.75),(0.75,0.75),(0.75,0.25)]
            Shape = sg.Box(corners)
            warnings.warn("No points list given for Polygon, using default list: %s." % corners)
        
                       
        else:
            assert len(corners) == 4, "Corners parameter has %s corners. A box must have 4 corners."%len(corners)  
            Shape = sg.Polygon(corners)
        
        if text_loc == None:
            text_loc = (Shape.centroid.x,Shape.centroid.y)
        else:
            text_loc = text_loc
        
        Area = Shape.area
        
        
        
        self.events[name] = dict(figure=shapely.affinity.rotate(Shape,angle),
                                fill_color=fill_color, alpha=alpha, text=text, 
                                text_loc=text_loc,fontsize=fontsize,
                                fontcolor=fontcolor,area=Area) 
        
    def add_Text(self,name,loc,text,fontsize,fontcolor):
        
        self.additional_text[name] = dict(loc=loc,text=text,
                                    fontsize=fontsize,fontcolor=fontcolor)

                
                
        
    def get_event_Area(self,ev_name):       
        return self.events[ev_name]['area']
    
#     def scatter_Points(self):
#         cos_angle = np.cos(np.radians(180.-angle))
#         sin_angle = np.sin(np.radians(180.-angle))

#         xc = x - g_ell_center[0]
#         yc = y - g_ell_center[1]

#         xct = xc * cos_angle - yc * sin_angle
#         yct = xc * sin_angle + yc * cos_angle 

#         rad_cc = (xct**2/(g_ell_width/2.)**2) + (yct**2/(g_ell_height/2.)**2)

#         colors_array = []

#         for r in rad_cc:
#             if r <= 1.:
#                 # point in ellipse
#                 colors_array.append('green')
#             else:
#                 # point not in ellipse
#                 colors_array.append('black')

#         ax.scatter(x,y,c=colors_array,linewidths=0.3)
        
    def events(self,name):
        return self.events[name]['figure']
              
        
    def plot_Sets(self,title,figsize=5,partition=False,text_box=None):
        '''
        Plot the set and subsets of a probability simulation.
        title: string, title of the chart.
        figsize: int, size of plot. Default 5.
        partition: bool, choose if the sets are partitioned. Default False.
        text_box: text box, a dictionary of the form dict(facecolor=matplotlib color, alpha=int).
        '''
        
        def cascade_split(to_split,splitters): #Helper function for partitions
            '''
            Return a list of all intersections between multiple polygons.
            to_split: list, polygons or sub-polygons to split
            splitters: list, polygons used as splitters
            
            Returns a list of all the polygons formed by the multiple intersections.
            '''
    
            if len(splitters) == 0:
                return to_split

            new_to_split = []

            for ts in to_split:
                f = split(ts,splitters[0].boundary)
                for i in list(f):
                    new_to_split.append(i)
            splitters.remove(splitters[0])

            return cascade_split(new_to_split,splitters)


        plt.figure(figsize=(figsize,figsize))
        plt.title(title)
        ax = plt.gca()
        ax.text(0.04,0.96,'$\Omega$',fontsize=9.5,horizontalalignment='right')
        
        if partition == True:
            
            #code by @Mike T @ stackexchange: https://gis.stackexchange.com/users/1872/mike-t
            
            event_list = [self.events[e]['figure'] for e in self.events]
            back_event_list = event_list[::-1]
            
            index_count = 0
            polys = []

            for i in combinations(event_list,len(event_list)-1): 
                c_split = cascade_split([back_event_list[index_count]],list(i))
                
                for p in c_split:
                    if not any(poly.equals(p) for poly in polys):
                        polys.append(p)
                index_count += 1
            
            partitions = {}
            
            for pol in range(len(polys)):
                partitions[pol+1] = dict(part=polys[pol],
                                       text='%s' % (pol+1))
                               

            for p in partitions:    
                ax.add_patch(descartes.PolygonPatch(partitions[p]['part'], 
                                                    fc=np.random.rand(3), 
                                                    ec=None, 
                                                    alpha=0.3))
                ax.text(partitions[p]['part'].centroid.x,partitions[p]['part'].centroid.y,
                            partitions[p]['text'],fontsize=10,
                            bbox=text_box,
                            color='blue',
                            horizontalalignment='center')  
            
            self.partitions = partitions
            
                                                   
        else:
            for e in self.events:
                ax.add_patch(descartes.PolygonPatch(self.events[e]['figure'], 
                                                    fc=self.events[e]['fill_color'], 
                                                    ec=None, 
                                                    alpha=self.events[e]['alpha']))
                
                                                                                                         
                ax.text(self.events[e]['text_loc'][0],self.events[e]['text_loc'][1],
                        self.events[e]['text'],fontsize=self.events[e]['fontsize'],
                        bbox=text_box,
                        color=self.events[e]['fontcolor'],
                        horizontalalignment='center')
        
        for text in self.additional_text:        
            ax.text(self.additional_text[text]['loc'][0],self.additional_text[text]['loc'][1],
            self.additional_text[text]['text'],fontsize=self.additional_text[text]['fontsize'],
            bbox=text_box,
            color=self.additional_text[text]['fontcolor'],
            horizontalalignment='center')
            
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        

        plt.show()
        
    def get_Partitions(self):
        if self.partitions == None:
            raise AttributeError("get_Partitions() failed. The sets are not partitioned.                                  \nUse parameter 'partition' = True in plot_Sets().")
        else:
            return self.partitions
            