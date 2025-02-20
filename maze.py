import matplotlib.pyplot as plt
import numpy as np
import turtle
import time
from frontier import Stack, Queue, QueueSort, HeapSort

FREE=0
BUSY=1

def trans(vec,coord=(0,0,0)):
	mat=np.array([[1,0,0,coord[0]],
					[0,1,0,coord[1]],
					[0,0,1,coord[2]],
					[0,0,0,1]])
	return np.matmul(mat,vec)

class Node:
	def __init__(self, pos, parent, action, value, shape):
		self.pos = pos
		self.parent = parent
		self.action = action
		self.value = value
		self.shape = shape
		self.level = 0 if parent is None else parent.level+1

class Maze:
	def __init__(self,map_file,size_pixel,pos_initial,pos_goal,type_distance='manhattan',type_search='bfs',sort='deafult',show_search=True):
		im = plt.imread(map_file)
		white=np.array([1., 1., 1., 1.])
		self.map=[[FREE if np.array_equal(im[i][j],white) else BUSY\
			for j in range(im.shape[1])]\
				for i in range(im.shape[0])]
		self.map=(np.array(self.map))[:][::-1].T
		self.memory=np.zeros(self.map.shape)
		self.size_pixel=size_pixel
		self.pos_initial=pos_initial #id
		self.memory[pos_initial[0]][pos_initial[1]]=BUSY
		self.pos_goal=pos_goal #id
		self.shape_goal=self.build_goal()
		self.visited=[]
		self.type_distance=type_distance #'euclidean', 'manhattan'
		self.type_search=type_search #'bfs', 'dfs', 'greedy', 'a*'
		self.sort=sort #'default', 'heap' -> work only with 'greedy', 'a*'
		self.solution=[]
		self.show_search=show_search
	

	def id_to_coord(self,pos):
		x=(pos[0]*self.size_pixel - self.map.shape[0]*self.size_pixel/2) + (self.size_pixel/2)
		y=(pos[1]*self.size_pixel - self.map.shape[1]*self.size_pixel/2) + (self.size_pixel/2)
		return (x,y)
	

	def build_shape(self,pos):
		l=self.size_pixel*0.8
		#Building square
		theta=np.linspace(0,2*np.pi,4,endpoint=False)
		vertices=[[(l/2)*(np.cos(i)-np.sin(i)),
				(l/2)*(np.cos(i)+np.sin(i)),
				0,
				1] for i in theta]
		shape=np.array(vertices)
		coord_pos=self.id_to_coord(pos)
		for i,point in enumerate(shape):
			shape[i]=trans(point,(coord_pos[0],coord_pos[1],0))
		return shape
	

	def build_goal(self):
		r=self.size_pixel*0.8/2
		#Building circle
		theta=np.linspace(0,2*np.pi,10,endpoint=False)
		vertices=[[r*np.cos(i),
				r*np.sin(i),
				0,
				1] for i in theta]
		self.shape_goal=np.array(vertices)
		coord_pos_goal=self.id_to_coord(self.pos_goal)
		for i,point in enumerate(self.shape_goal):
			self.shape_goal[i]=trans(point,(coord_pos_goal[0],coord_pos_goal[1],0))
		return self.shape_goal


	def neighbors(self,node):
		col,row = node.pos
		children=[]
		#UP
		if (row+1<self.map.shape[1]) and\
		   (self.map[col][row+1]==FREE) and\
		   (self.memory[col][row+1]==FREE):
			children.append(("up", (col, row+1)))
			self.memory[col][row+1]=BUSY
		#Down
		if (row-1>=0) and\
		   (self.map[col][row-1]==FREE) and\
		   (self.memory[col][row-1]==FREE):
			children.append(("down", (col, row-1)))
			self.memory[col][row-1]=BUSY
		#Right
		if (col+1<self.map.shape[0]) and\
		   (self.map[col+1][row]==FREE) and\
		   (self.memory[col+1][row]==FREE):
			children.append(("right", (col+1, row)))
			self.memory[col+1][row]=BUSY
		#Left
		if (col-1>=0) and\
		   (self.map[col-1][row]==FREE) and\
		   (self.memory[col-1][row]==FREE):
			children.append(("left", (col-1, row)))
			self.memory[col-1][row]=BUSY
		return children


	def distance(self,pos,level=0):
		if self.type_distance=='manhattan':
			value=abs(self.pos_goal[0]-pos[0])+abs(self.pos_goal[1]-pos[1])
		elif self.type_distance=='euclidean':
			value=np.sqrt((self.pos_goal[0]-pos[0])**2+(self.pos_goal[1]-pos[1])**2)
		else:
			value=0

		if self.type_search=='a*':
			value+=level
		return value

	@staticmethod
	def draw_face(shape,color,pen):
		pen.setpos(shape[0][0],shape[0][1])
		pen.down()
		pen.color('black',color)
		#pen.fillcolor(color)
		pen.begin_fill()
		for point in shape[1:]:
			pen.goto(point[0],point[1])
		pen.goto(shape[0][0],shape[0][1])
		pen.end_fill()
		pen.up()
		
	def draw_maze(self,frontier,pen):
		self.draw_face(self.shape_goal,'blue',pen)
		for node in self.visited:
			self.draw_face(node.shape,'green',pen)
		if not frontier is None:
			for node in frontier.frontier:
				self.draw_face(node.shape,'red',pen)
	
	def draw_solution(self,pen):
		for node in self.solution:
			self.draw_face(node.shape,'green',pen)
	
	def solve(self,win,pen):
		self.num_explored = 0
		start = Node(pos=self.pos_initial,
			         parent=None,
					 action=None, 
					 value=self.distance(pos=self.pos_initial,level=0),
					 shape=self.build_shape(self.pos_initial))
		
		if self.type_search=='dfs':
			frontier = Stack()
		elif self.type_search=='bfs':
			frontier = Queue()
		elif (self.type_search=='greedy' or self.type_search=='a*') and self.sort=='default':
			frontier = QueueSort()
		elif (self.type_search=='greedy' or self.type_search=='a*') and self.sort=='heap':
			frontier = HeapSort()

		frontier.add(start)

		while True:
			if frontier.empty():
				raise Exception("No solution")

			node = frontier.remove()
			#print(node.pos)
			self.visited.append(node)
			self.num_explored += 1

			if node.pos == self.pos_goal:
				while node.parent is not None:
					self.solution.append(node)
					node = node.parent
				self.solution.append(node)
				self.solution.reverse()
				return
				
			for action, pos in self.neighbors(node):
				child = Node(pos=pos,
			         		 parent=node,
					    	 action=action, 
					 	     value=self.distance(pos=pos,level=node.level+1),
					 		 shape=self.build_shape(pos))
				frontier.add(child)
			
			if self.show_search:
				pen.clear()
				self.draw_maze(frontier,pen)
				#time.sleep(0.01)
				win.update()	

if __name__=='__main__':
	map_file='maze.png'
	map_bg='maze_bg.png'
	maze=Maze(map_file=map_file,
		      size_pixel=20,
			  pos_initial=(0,49),
			  pos_goal=(49,0),
			  type_distance='euclidean', #euclidean, manhattan
			  type_search='greedy',
			  sort='heap',
			  show_search=True)

	win=turtle.Screen()
	win.setup(maze.map.shape[0]*maze.size_pixel,maze.map.shape[1]*maze.size_pixel)
	win.bgpic(map_bg)
	win.title('Maze')
	win.tracer(0)
	my_pen=turtle.Turtle()
	my_pen.hideturtle()
	my_pen.up()
	
	maze.solve(win,my_pen)
	my_pen.clear()
	maze.draw_solution(my_pen)
	print('Length of way:',len(maze.solution))
	print('Positions explored:',maze.num_explored)
	win.update()
	#time.sleep(0.1)
	turtle.done()
