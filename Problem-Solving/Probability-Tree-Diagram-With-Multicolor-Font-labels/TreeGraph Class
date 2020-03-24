import networkx as nx
import random

import chart_studio.plotly as ply
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
import plotly.io as pio

# remove the default background theme for the plot
pio.templates.default = "none"

def build_nodeDict(elements,repeat,children):
    '''
    Helper Funtion used to create a dictionary of nodes that can be used
    with the TreeGraph class below.
    elements: string or list of ints or floats with the items to be combined
    repeat: int number of times to repeat the same item in the combination
    children: list of lists where each list contains the int reference of the
            children in a node. Node is referenced as the index of the outer list (node 0 = index 0).  
            If the node has no children, instead of a list a 'None' value is expected.
    Returns a dictionary of nodes => values
    '''
    from itertools import product
    
    nodes = {}
    
    combos = product(elements,repeat=repeat)
    key = 0
    used = []
    for i in range(len(elements)**repeat): #The final branches of the tree have len(elements)^repeat results.

        c = next(combos) #choose next item in the iterator
        s = '' #Create each node as a string

        for x in c: 
            if type(x) != str:
                x = str(x)
            else:
                if key == 0: #node 0 is the root, so it has no item associated with it.
                    nodes[key] = ('',children[key])
                    key +=1

                s += x
                if s not in used: #Avoid adding the same combination
                    nodes[key] = (s,children[key])
                    used.append(s)
                    key +=1
        s = ''#Reset s to empty for a new combo to be processed.
        
    return nodes

class TreeGraph:
    '''
    Hierarchical graph class using the networkx package (https://networkx.github.io/)  
    for processing the graph information needed to visualize it using
    the plotly package (https://plot.ly/).
    '''
    
    def __init__(self,orientation='v', root=None, nodes={}, spread=0.3, gap=0.01, root_x=None, 
                 root_y=None, edge_weights=None, edge_labels=None, pos=None, parent=None):
            '''
            orientation: string or None. Direction of the graph given as 'v'(vertical, 
                         top-down hierarchy) or 'h'(horizontal, left-right hierarchy)
                         Default is None and it produces a vertical graph.

            root: the root node of current branch 
            - if the tree is directed and this is not given, 
              the root will be found and used
            - if the tree is directed and this is given, then 
              the positions will be just for the descendants of this node.
            - if the tree is undirected and not given, 
              then a random choice will be used.

            nodes: dictionary of nodes by key(int)->(node name(str),node children(list)).
                   The keys need to follow a numerical order, where lowest int is the root and largest
                   int is the furthest node.
            
            spread: horizontal or vertical space allocated for this branch - avoids overlap with other branches

            gap: gap between levels of hierarchy

            root_x: horizontal location of root

            root_y: vertical location of root
            
            edge_weights: dictionary of edges where key is a string concatenating two nodes from nodes dict
                          and value is an integer with the edge's weight. 
                          key(str(nodes[parent int])+str(nodes[child int]))->weight(int)
            
            edge_labels: dictionary of edges where key is a string concatenating two nodes from nodes dict
                         key(str(nodes[parent int])+str(nodes[child int]))->label(str)
            
            pos: a dict saying where all nodes go if they have been assigned
            parent: parent of this branch. - only affects it if non-directed
            
            A networkx graph object, self.G, a tree, is created using the data in 'nodes'.
            '''
            self.G = nx.Graph()
            self.orientation = orientation
            self.root = root
            self.nodes = nodes
            self.spread = spread
            self.gap = gap
            
            if (self.orientation == 'v' and (root_x == None or root_y == None)):
                self.root_x = 0.5
                self.root_y = 0
            elif (self.orientation == 'h' and (root_x == None or root_y == None)):
                self.root_x = 0
                self.root_y = 0.5
            else:
                self.root_x = root_x
                self.root_y = root_y
             
            self.edge_weights = edge_weights
            self.edge_labels = edge_labels
            self.pos = pos
            self.parent = parent
            
            self.edge_list = [] #List of edges to add to networkx graph
            self.edge_Outlabels = {} #Dictionary of labels assigned to each edge
            for parent in self.nodes:
                try:
                    for child in self.nodes[parent][1]:
                        try:
                            if self.edge_weights != None:
                                self.edge_list.append((self.nodes[parent][0],self.nodes[child][0],
                                                       self.edge_weights['%s%s'%(parent,child)]))
                            else:
                                self.edge_list.append((self.nodes[parent][0],self.nodes[child][0]))
                                
                            self.edge_Outlabels[(self.nodes[parent][0],self.nodes[child][0])] = \
                            self.edge_labels['%s%s'%(parent,child)]
                        except TypeError:
                            continue
                except TypeError:
                            continue
            
            if self.edge_weights != None: #add weighted edges if provided
                self.G.add_weighted_edges_from(self.edge_list)
           
            else: #add edges
                self.G.add_edges_from(self.edge_list)
   
    def nx_Graph(self):
        '''
        Returns the networkx graph.
        '''
        return self.G 
    
    def edge_weights(self):
        return self.edge_weights
    
    def edge_lbls(self):
        return self.edge_Outlabels #returns the edge labels
    
    def hierarchy_pos(self):
        '''
        Modification of Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
        Licensed under Creative Commons Attribution-Share Alike 

        If the graph is a tree this will return the positions to plot this in a 
        hierarchical layout.
        
        Returns a dictionary with the hierarchy positions for a vertical tree or a horizontal tree.
        '''

        if not nx.is_tree(self.G): #NODES NAMES MUST BE ALL DIFFERENT or else it won't create a tree
            raise TypeError('cannot use hierarchy_pos on a graph that is not a tree') 

        if self.root is None:
            if isinstance(self.G, nx.DiGraph):
                self.root = next(iter(nx.topological_sort(self.G)))  #allows back compatibility with nx version 1.11
            else:
                self.root = random.choice(list(self.G.nodes))

        def _hierarchy_pos(G, root, spread, gap, root_x, root_y, pos=None, parent=None):

            if pos is None:
                pos = {root:(root_x, root_y)}
            else:
                pos[root] = (root_x, root_y)
            children = list(G.neighbors(root))
            if not isinstance(G, nx.DiGraph) and parent is not None:
                children.remove(parent)  
            if len(children)!=0:
                sp = spread/len(children) #sp divides the spread by all children
                nextxV = root_x - spread/2 - sp/2
                nextxH = root_y + spread/2 + sp/2
                for child in children:
                    if self.orientation == 'v':
                        nextxV += sp #Next horizontal position for a Vertical graph
                        pos = _hierarchy_pos(G,child, spread=sp, gap=gap, 
                                            root_x=nextxV,root_y=root_y-gap,
                                            pos=pos, parent = root)
                    elif self.orientation == 'h':
                        nextxH -= sp #Next horizontal position for a Horizontal graph
                        pos = _hierarchy_pos(G,child, spread=sp, gap=gap, 
                                             root_y=nextxH,root_x=root_x+gap,
                                             pos=pos, parent = root)
                    else:
                        raise Exception("Not a valid command for variable orientation! \n\
                        A string is needed with the value 'v' for a vertical graph (top-down) or \n\
                        value 'h' for horizontal graph (left-right). Default is 'v'.")
            return pos

        return _hierarchy_pos(self.G, self.root, self.spread, self.gap, 
                              self.root_x, self.root_y, self.pos, self.parent)
    
    def get_MaxLevels(self):
        '''
        Returns an int representing the maximun number of levels of hierarchy following
        the longest path of the Tree, from root to furthest node.
        '''
        depth=None
        for p in nx.all_simple_paths(self.G,#returns a path from source to destination
                                     list(self.G.nodes)[0],
                                     list(self.G.nodes)[-1]):
            depth = p
    
        return len(depth)
    
    def get_Descendants(self):
        '''
        Returns a set with all descendants of the Tree's root.
        '''      
        return nx.descendants(self.G,self.nodes[0][0])       
    
    def get_PlotLayoutAxisInf(self):
        '''
        Gets the Layout axis information to accommodate the graph in a 
        proper x and y position when plotting. Returns a dictionary.
        '''
        pos = self.hierarchy_pos().values()
        x_values = [v[0] for v in pos]
        y_values = [v[1] for v in pos]
        
        if self.orientation == 'v':
            xRange = [min(x_values)-0.09, max(x_values)+0.09]
            yRange = [min(y_values)-0.006, max(y_values)]
            height = self.get_MaxLevels()*99 #height in pixels for the vertical plot space.
            width = len(self.get_Descendants())*133 #width in pixels for the vertical plot space.
        else:
            xRange = [min(x_values)-0.01, max(x_values)+0.45]
            yRange = [min(y_values)-0.1, max(y_values)+0.1]
            height = len(self.get_Descendants())*66 #height in pixels for the horizontal plot space.
            width = self.get_MaxLevels()*300 #width in pixels for the horizontal plot space.
            
        x_axis = dict(range=xRange, showgrid=False, zeroline=False, showticklabels=False)
        y_axis = dict(range=yRange, showgrid=False, zeroline=False, showticklabels=False)
        
        return {'x_axis':x_axis, 'y_axis':y_axis, 'height':height, 'width':width}
    
    def edge_midpoint(self,nStart,nEnd):      
        '''
        Returns the midpoint of a given edge given its start -> end nodes.
        nStart = start node tuple, nEnd = end node tuple
        returns: a tuple, edge midpoint with x,y coordinates.
        '''
        mid = ((nStart[0]+nEnd[0])/2,(nStart[1]+nEnd[1])/2)
        return mid
    
    def node_traces(self,pos,root_trace,node_trace,node_Mcolor='white'):
        '''
        Provides the information of the plotly traces for nodes.
        pos: position of nodes
        root_trace: the root plotly trace settings
        node_trace: the node plotly trace settings
        node_Mcolor: assign a color to the node, default white
        
        Adds data to the plotly traces. Traces have to be created prior using plotly.
        '''
        for node in self.G.nodes():
            x, y = pos[node]
            if node == '':
                root_trace['x'] += tuple([x])
                root_trace['y'] += tuple([y])
            else:        
                node_trace['x'] += tuple([x])
                node_trace['y'] += tuple([y])
                node_trace['text']+=tuple([node])
                node_trace['marker']['color']+=tuple([node_Mcolor])
            
    def edge_traces(self,pos,edge_trace):
        '''
        Provides the information of the plotly traces for edges lines and labels.
        pos: position of nodes
        edge_trace: the edge plotly trace settings
        
        Adds data to the plotly traces. Traces have to be created prior using plotly.
        '''
        for edge in self.G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
            
    def paths_product(self,source,target):
        '''
        Return the product of a path from node 'source' to node 'target'
        (Multiplies the weight of each edge).
        
        source: An integer, the source node, as the key given in the 'nodes' dictionary.
        target: An integer, the target node, as the key given in the 'nodes' dictionary.
        
        Returns the product of all weights in the path.
        '''
        
        path_edge_list = None
        paths = nx.all_simple_paths(self.G,self.nodes[source][0],self.nodes[target][0])
        for path in map(nx.utils.pairwise, paths):
            path_edge_list = list(path)

        product = 1
        for edge in path_edge_list:
            product *= self.G.get_edge_data(edge[0],edge[1])['weight']
            
        return product
    
    def G_custom_legend(self,xpos=None,ypos=None,names={},des_gap=0.02,vert_gap=0.13):
        '''
        Create a custom legend for the graph.
        xpos: int or float for the x-axis position of the legend's box top left corner.
        ypos: int or float for the y-axis position of the legend's box top left corner.
        names: dictionary of all legend symbol => symbol description. Default is an empty dict.
        des_gap: int for the gap between the legend symbol and its text description. Default is 0.02.
        vert_gap: float/int. Vertical gap between legend items. Default for horizontal tree is 0.13.
                  Recommended for vertical tree is 0.0009.

        Returns a list of dictionaries, 2 dictionaries for each Graph symbol.
        '''
        
        if len(names) == 0:
            names = {"[*]":"[Custom legend goes here,]",
                     "[**]":"[set using 'names' parameter]"}
        
        vals = list(self.hierarchy_pos().values())
        
        if self.orientation == 'v':
            
            if xpos == None and ypos == None:
                xpos = min(list(zip(*vals))[0])-0.045 #zip is used to pair values from different lists. 
                ypos = max(list(zip(*vals))[1]) #The * unzips the values.

            else:
                xpos = xpos
                ypos = ypos
            
        else:
            if xpos == None and ypos == None:
                xpos = max(list(zip(*vals))[0])+0.15
                ypos = max(list(zip(*vals))[1])/2

            else:
                xpos = xpos
                ypos = ypos

        legend = [] 
        
        for name in names:
            legend.append(dict(x=xpos,y=ypos,text=name,showarrow=False,xanchor='left'))
            legend.append(dict(x=xpos+des_gap,y=ypos,text=names[name],showarrow=False,xanchor='left'))
            
            ypos -= vert_gap #Vertical gap default is for horizontal Tree. Adjust accordingly.

                                                  
        return legend


    def generic_plotly_plot(self, title, title_pos=0.05, height=None, width=None, notebook_mode=True,
                            node_fontsize=12, legend=False,legend_labels=None,legnd_pos=None,
                            leg_des_gap=0.02,leg_vert_gap=0.13, label_fontsize=11):
        '''
        Helper function with generic plotly settings for a basic plot using 
        the TreeGraph() class instance settings.

        title: str with graph title.
        title_pos: float or int, move the title position along the x-axis
        height: int, Graph height in pixels. Default None.
        width: int, Graph width in pixels. Default None.
        notebook_mode: bool, allow a plotly plot to be shown in a Jupyter Notebook.
        legend: bool, if True show legend using lagend_labels.
        legend_labels: dictionary of all legend symbol => symbol description. Default is None.
        legnd_pos: tuple(xval,yval)
        leg_des_gap: int/float for the gap between the legend symbol and its text description. Default is 0.02.
        leg_vert_gap: float/int. Vertical gap between legend items. Default for horizontal tree is 0.13.
                      Recommended for vertical tree is 0.0009.
        label_fontsize: int/float fontsize for labels
        '''  

        init_notebook_mode(connected=notebook_mode) #Allow plotly to plot inside notebook

        layoutDefaults = self.get_PlotLayoutAxisInf() #Inserts height, width, xaxis and yaxis settings for graph.

        if height == None:
             height = layoutDefaults['height']

        if width == None:
             width = layoutDefaults['width']


        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.9,color='#777'),
            text=[],
            mode='lines')

        self.edge_traces(self.hierarchy_pos(),edge_trace) #Fill edge_trace

        root_trace = go.Scatter(
            x=[],
            y=[], 
            text=[],
            mode='text',
            marker=dict(
                showscale=False,
                color=[],
                size=0))

        node_trace = go.Scatter(
            x=[],
            y=[], 
            text=[],
            textfont=dict(size=node_fontsize),
            mode='markers+text',
            name='Nodes',
            showlegend=False,
            marker=dict(
                symbol = 'diamond-wide',
                showscale=False,
                color=[],
                size=70))

        self.node_traces(self.hierarchy_pos(),root_trace,node_trace) #Fill root_trace and node_trace 

        annotations = []
     
        if legend == True:
            if legnd_pos == None:
                legend_function = self.G_custom_legend(names=legend_labels) #Use the G_custom_legend() method 
            else:
                legend_function = self.G_custom_legend(xpos=legnd_pos[0],ypos=legnd_pos[1],names=legend_labels,
                                                       des_gap=leg_des_gap,vert_gap=leg_vert_gap)
            
            for l in legend_function:
                annotations.append(l) #add each element of the G_custom_legend() list to annotations.
                
        if self.edge_labels == None:
            annotations = None
        else:
            for edge in self.nx_Graph().edges(): 
                label = self.edge_midpoint(self.hierarchy_pos()[edge[0]],self.hierarchy_pos()[edge[1]])
                annotations.append(dict(x=label[0],y=label[1],xref='x',yref='y',text=self.edge_lbls()[edge],
                                       showarrow=True,borderpad=1,align='center',ax=3,ay=-5,arrowsize=1,arrowwidth=1,
                                       font=dict(size=label_fontsize,color='#333')))


        fig = go.Figure(data=[root_trace,edge_trace, node_trace],
                        layout=go.Layout(
                        annotations=annotations,
                        hovermode='closest', #Show closest data on hover
                        autosize=True,
                        height=height, #Use layoutDefaults or costumize your own size
                        width= width,               
                        title=go.layout.Title(text=title,x=title_pos),
                        titlefont=dict(size=16),
                        showlegend=False,
                        margin=dict(b=0,l=0,r=0,t=30),
                        xaxis= layoutDefaults['x_axis'],
                        yaxis= layoutDefaults['y_axis']))

        iplot(fig)

        
# EXAMPLE OF TreeGraph INSTANCE PROVIDING NODES AND EDGE LABELS

# radar_nodes = {0:('',[1,2]),
#                1:('$\color{blue}{\LARGE A}$',[3,4]),
#                2:('$\color{blue}{\LARGE A^c}$',[5,6]),
#                3:('$\color{blue}{\LARGE A}\LARGE \cap\color{red}{\LARGE B}$',None),
#                4:('$\color{blue}{\LARGE A}\LARGE \cap\color{red}{\LARGE B^c}$',None),
#                5:('$\color{blue}{\LARGE A^c}\LARGE \cap\color{red}{\LARGE B}$',None),
#                6:('$\color{blue}{\LARGE A^c}\LARGE \cap\color{red}{\LARGE B^c}$',None)}

# edge_labels = {'01':'$P(\color{blue}{A})\\\ 0.05$',
#                '02':'$P(\color{blue}{A^c})\\\ 0.95$',
#                '13':'$P(\color{red}{B}|\color{blue}{A})\\\ 0.99$',
#                '14':'$P(\color{red}{B^c}|\color{blue}{A})\\\ 0.01$',
#                '25':'$P(\color{red}{B}|\color{blue}{A^c})\\\ 0.1$',
#                '26':'$P(\color{red}{B^c}|\color{blue}{A^c})\\\ 0.90$'}

# G = TreeGraph(orientation='h',root=radar_nodes[0][0],spread=0.4,gap=0.13,nodes=radar_nodes,edge_labels=edge_labels)
# G.generic_plotly_plot("Radar Probability of Detecting a Plane", 
                    title_pos=0.05, height=400, width=None,legend=False)

