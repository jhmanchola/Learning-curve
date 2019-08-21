#!/usr/bin/env python
# coding: utf-8

import networkx as nx
# import matplotlib.pyplot as plt


class SystemLayout(object):
    '''
    Create a system of nodes in the style of a horizontal tree, 
    using orthogonal lines as edges. This class relies on the networkx
    package (https://networkx.github.io/) to generate a graph.
    '''

    def __init__(self,root,root_pos,units,gap,pos=None):      
        '''
        Initialize an instance with the following values:
        root: the root of the tree as a tuple of (node name, [list of children]).
        root_pos: the position of the root as a tuple of (X value, Y value).
        units: a dictionary of nodes and empty nodes with a tuple value with the following:
                   (node name,
                    [list of children or None if missing],
                    string representing orientation of node where
                    'N'=North, 'S'=South, 'E'=East, 'W'=West)
              An empty node is just a point in the graph that will help create a 90° break in the orthogonal edge.
        gap: float or int representing the space between nodes
        pos: dictionary of node positions used by networkx to create the graph. node->(X value, Yvalue)
        '''  
        
        self.S = nx.Graph()
        self.root = root
        self.root_pos = root_pos
        self.units = units
        self.gap = gap
        self.pos = pos
        
        def Get_Pos_and_Paths(root,root_pos,units,gap,pos=None,paths=[]):

            def Get_dict_keys(d, val):
                return [k for k in d.keys() if d[k] == val]

            if pos==None:
                pos = {root[0]:root_pos}
#                 Xval = pos[root[0]][0]
#                 Yval = pos[root[0]][1]
#                 orient = {'N':(Xval,Yval+gap), 'S':(Xval,Yval-gap), 
#                           'E':(Xval+gap,Yval), 'W':(Xval-gap,Yval)}

            else:
                pos = pos  
            
            Xval = pos[root[0]][0]
            Yval = pos[root[0]][1]
            orient = {'N':(Xval,Yval+gap), 'S':(Xval,Yval-gap), 
                      'E':(Xval+gap,Yval), 'W':(Xval-gap,Yval)}
                
            paths = paths

            new_root = root
            try:

                for child in root[1]:
                    node = units[child][0]
                    pos[node] = orient[units[child][2]]       
                    new_root = units[child]
                    paths.append([root[0],node])
                    pos = Get_Pos_and_Paths(new_root,pos[new_root[0]],units,gap,pos=pos,paths=paths)[0]

            except TypeError:
                new_root = root
                Get_key = Get_dict_keys(units, new_root)[0]
                node = new_root[0]
                pos[node] = orient[units[Get_key][2]]       
                new_root = units[Get_key]
           

            return pos,paths 
        
        self.pos_paths = Get_Pos_and_Paths(self.root,self.root_pos,self.units,self.gap,
                                     self.pos,paths=[])
        
        self.nx_pos = self.pos_paths[0]
        self.nx_paths = self.pos_paths[1]

  
    def get_nxGraph(self):
        return self.S
    
    def get_Pos(self):
        return self.nx_pos
    
    def get_Paths(self):   
        return self.nx_paths
    
    def draw_nx(self,empty_root=False,node_size=600,node_color='lightskyblue',
                bordercolors='k',edge_color='k',font_size=14,font_color='k'):
            
        color = 0    
        pos = self.get_Pos()
        paths = self.get_Paths()
        
        for n in self.units:
            nname = self.units[n][0]
            if (type(n) != int) or ((self.units[n][0]=='root') and (empty_root==True)):
                nx.draw(self.S,pos=pos,nodelist=[nname],node_shape='',node_size=0)
                
            elif type(node_color) == list: 
                if type(font_color) == list:
                    nx.draw(self.S,pos=pos,nodelist=[nname],node_color=node_color[color],node_size=node_size,
                            node_shape='s',edgecolors=bordercolors,labels={nname:nname},with_labels=True,
                            edgelist=paths,edge_color=edge_color,font_size=font_size,font_color=font_color[color])
                    color += 1
                else:
                    nx.draw(self.S,pos=pos,nodelist=[nname],node_color=node_color[color],node_size=node_size,
                            node_shape='s',edgecolors=bordercolors,labels={nname:nname},with_labels=True,
                            edgelist=paths,edge_color=edge_color,font_size=font_size,font_color=font_color)
                    color += 1
            else:
                nx.draw(self.S,pos=pos,nodelist=[nname],node_color=node_color,node_size=node_size,
                        node_shape='s',edgecolors=bordercolors,labels={nname:nname},with_labels=True,
                        edgelist=paths,edge_color=edge_color,font_size=font_size,font_color=font_color)
            
        
        for path in paths:
            self.S.add_path(path)    


# # EXAMPLE


# units = {0:('root',[1]),
#         1:(r'$P_1$',['empty 0'],'E'),
#         'empty 0':('empty 0',['empty 1','empty 2'],'E'), 
#         'empty 1':('empty 1',[2],'N'),
#         2:(r'$P_2$',['empty 3'],'E'),
#         'empty 2':('empty 2',[3],'S'),
#         3:(r'$P_3$',['empty 6'],'E'),
#         'empty 3':('empty 3',['empty 4'],'E'),
#         'empty 4':('empty 4',['empty 5'],'S'),
#         'empty 5':('empty 5',None,'E'),
#         'empty 6':('empty 6',['empty 7'],'E'),
#         'empty 7':('empty 7',None,'N')}

# root = units[0]


# F = SystemLayout(root,(0,0.5),units,0.005,pos=None)
# F.draw_nx(empty_root=True,node_size=2500,node_color='lightskyblue')