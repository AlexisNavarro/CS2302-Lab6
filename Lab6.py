# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 22:34:58 2019

@author: Alexis Navarro
CS 2302
Olac Fuentes
Purpose:The purpose of this lab is to be able to work with disjoint set forests while applying it to create a maze.
        I have to be able to remove random walls in order to create a path from the square 0 to the square 149 (Shown in figure 1).
        To do this I need to get the amount of sets which will be used to remove a wall, make a disjoint set forest by using the rows and columns,
        Then I need to make the remove function after all the other parts are made.   
"""


import matplotlib.pyplot as plt
import numpy as np
import random



#GIVEN FUNCTIONS (PROVIDED BY CS 2302)

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])



def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j) 
    if ri!=rj: # Do nothing if i and j belong to the same set 
        S[rj] = ri  # Make j's root point to i's root
        
def findC(S,i):
    if S[i]<0:
        return i
    r = findC(S,S[i])
    S[i]=r
    return r   

#combines the two set by using their size as reference
def union_by_Size(S,i,j):
    ri = findC(S,i)
    rj = findC(S,j)
    if ri!=rj: # Do nothing if i and j belong to the same set 
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri
   
#------------------------------------------------------------------------------
#MADE METHOD/FUNCTION REQUIRED TO ACCOMPLISH THE LAB
            
#method to count the amount of sets in the DSF
def setAmount(S):
    count=0
    for i in range(len(S)):
        if S[i]<0:
            count +=1
    return count

#method to delete random parts of the wall
def remove(S,maze_walls,numSets):
    while numSets > 1:
        w = random.choice(maze_walls)# w gets the wall that was randomly selected
        i=maze_walls.index(w)#gets the position where we chose the wall to delete
        if find(S,w[0]) != find(S,w[1]):
            maze_walls.pop(i) #deletes the wall
            union(S,w[0],w[1])# combines the walls after the deletion
            numSets-=1
    return w
            
#------------------------------------------------------------------------------
#METHOD TO DRAW THE MAZE (PROVIDED BY THE CS2302)
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)


    
def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w
plt.close("all") 

#------------------------------------------------------------------------------
#MAIN

#size of rows and columns (Dimensions of the maze)
maze_rows = 10
maze_cols = 15


maze_walls = wall_list(maze_rows,maze_cols)#Gets the list of walls in the maze


draw_maze(maze_walls,maze_rows,maze_cols,cell_nums=True) #calls the draw maze method and makes the complete maze without deletion


S = DisjointSetForest(maze_rows*maze_cols)# makes the new DSF by combining the rows and columns


numSets=setAmount(S) # gets the amount of sets in the maze


remove(S,maze_walls,numSets)# calls the method to remove parts of the wall


draw_maze(maze_walls,maze_rows,maze_cols)#draws the walls after the deletion of random maze walls