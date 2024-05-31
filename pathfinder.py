import pygame
import queue
black,green,red,blue=(0,0,0),(0,255,0),(255,0,0),(0,0,255)
width,height,tile_size=1920,1080,20
fps=60
grid_width=width//tile_size
grid_height=height//tile_size
screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()
def count_points(grid):
    s,f=0,0
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j]==2:s+=1
            elif grid[i][j]==3:f+=1
    return s,f
def draw_grid(lst):
    for i in range(0,len(lst)):
        for j in range(0,len(lst[0])):
            top_left=(tile_size * j , tile_size * i)
            if lst[i][j]==1:
                pygame.draw.rect(screen,black,(*top_left,tile_size,tile_size))
            elif lst[i][j]==2:
                pygame.draw.rect(screen,red,(*top_left,tile_size,tile_size))
            elif lst[i][j]==3:
                pygame.draw.rect(screen,green,(*top_left,tile_size,tile_size))   
            elif lst[i][j]==4:
                pygame.draw.rect(screen,blue,(*top_left,tile_size,tile_size))
def find_neighbors(maze,row,col):
    neighbors=[]
    if row>0:neighbors.append((row-1,col))
    if row+1<len(maze):neighbors.append((row+1,col))
    if col>0:neighbors.append((row,col-1))
    if col+1<len(maze[0]):neighbors.append((row,col+1))
    return neighbors                
def find(arr,target):
    for i in range(0,len(arr)):
        for j in range(0,len(arr[0])):
            if arr[i][j]==target:return i,j                  
def solve(lst):
    start_pos=find(lst,3)
    q=queue.Queue()
    q.put((start_pos,[start_pos]))
    visited=set()
    while not q.empty():
        current_pos,path=q.get()
        row,col=current_pos
        if lst[row][col]==2:return path
        neighbors=find_neighbors(lst,row,col)
        for n in neighbors:
            if n in visited:continue
            r,c=n
            if lst[r][c]==1:continue
            new_path=path+[n]
            q.put((n,new_path))
            visited.add(n)   
def main():
    holdrow,holdcol=-1,-1
    grid=[[0 for i in range(grid_width)] for j in range(grid_height)]
    running=True
    start_counter=0
    finish_counter=0
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                col=x // tile_size
                row = y // tile_size
                play=False
                if event.button==1:
                    if grid[row][col]==0:grid[row][col]=1
                    else:grid[row][col]=0
                elif event.button==3 or event.button==2:
                    if event.button==3 and start_counter==0:
                        if grid[row][col]==0 or grid[row][col]==1 :grid[row][col]=2
                        else:grid[row][col]=0  
                    if event.button==2 and finish_counter==0:
                        if grid[row][col]==0 or grid[row][col]==1 :grid[row][col]=3
                        else:grid[row][col]=0 
                    start_counter,finish_counter=count_points(grid)
            elif pygame.mouse.get_pressed()[0]==True:
                play=False
                x,y=pygame.mouse.get_pos()
                col=x // tile_size
                row = y // tile_size
                if pygame.mouse.get_pressed()[0]==True and (holdrow!=row or holdcol!=col):
                        if grid[row][col]==0:
                            grid[row][col]=1
                            holdrow,holdcol=row,col
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                if event.key==pygame.K_SPACE:
                    ans=solve(grid)
                    for i in ans:
                        r,c=i
                        grid[r][c]=4
                    print(ans)
        screen.fill((255,255,255))
        draw_grid(grid)
        pygame.display.update()
    pygame.quit()
main()