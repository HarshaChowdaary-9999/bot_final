from flask import Flask, Response, request
from random import choice
import copy
app = Flask(__name__)

def calculate_up(grid,depth):
  temp_score=0
  temp_up=grid
  while depth>0:
    for i in range(0,4):    
      for j in range(0,4):        
          if(temp_up[i][j] == 0):            
              for j_temp in range(j+1,4):
                  if(temp_up[i][j_temp]):                    
                      temp_up[i][j] = temp_up[i][j_temp]
                      temp_up[i][j_temp] = 0
                      
                      break
      for j in range(0,3):        
          if(temp_up[i][j] == temp_up[i][j+1] and temp_up[i][j] != 0):             
              temp_up[i][j] *= 2
              temp_score += temp_up[i][j]
              print('up check',temp_score)
              for j_temp in range(j+1,3):
                  temp_up[i][j_temp] = temp_up[i][j_temp+1]

              temp_up[i][3] = 0
    depth=depth-1
  print('cal up:',temp_score)
  return temp_score
        
def calculate_down(grid,depth):
  temp_score=0
  while depth>0:
    for i in range(0,4):    
      for j in range(3,-1,-1):        
          if(grid[i][j] == 0):              
              for j_temp in range(j-1,-1,-1):
                  if(grid[i][j_temp]):                      
                      grid[i][j] = grid[i][j_temp]
                      grid[i][j_temp] = 0                      
                      break 
      for j in range(3,0,-1):          
          if(grid[i][j] == grid[i][j-1] and grid[i][j] != 0):               
              grid[i][j] *= 2
              temp_score += grid[i][j]
              legal_move = 1
              for j_temp in range(j-1,0,-1):
                  grid[i][j_temp] = grid[i][j_temp-1]
              grid[i][0] = 0
    depth=depth-1
  print('cal down:',temp_score)
  return temp_score
def calculate_right(grid,depth):
  temp_score=0
  while depth>0:
    for i in range(0,4):    
      for j in range(3,-1,-1):        
          if(grid[j][i] == 0):              
              for i_temp in range(j-1,-1,-1):
                  if(grid[i_temp][i]):                      
                      grid[j][i] = grid[i_temp][i]
                      grid[i_temp][i] = 0                      
                      break 
      for j in range(3,0,-1):          
          if(grid[j][i] == grid[j-1][i] and grid[j][i] != 0):               
              grid[j][i] *= 2
              temp_score += grid[j][i]
              legal_move = 1
              for i_temp in range(j-1,0,-1):
                  grid[i_temp][i] = grid[i_temp-1][i]

              grid[0][i] = 0
    depth=depth-1 
  print('cal right:',temp_score)         
  return temp_score
def calculate_left(grid,depth):
  temp_score=0
  while depth>0:
    for i in range(0,4):    
      for j in range(0,4):        
          if(grid[j][i] == 0):              
              for i_temp in range(j+1,4):
                  if(grid[i_temp][i]):                      
                      grid[j][i] = grid[i_temp][i]
                      grid[i_temp][i] = 0                      
                      break                
      for j in range(0,3):          
          if(grid[j][i] == grid[j+1][i] and grid[j][i] != 0):               
              grid[j][i] *= 2
              temp_score += grid[j][i]
              legal_move = 1
              for i_temp in range(j+1,3):
                  grid[i_temp][i] = grid[i_temp+1][i]
              grid[3][i] = 0
    depth=depth-1
  print('cal left :',temp_score)  
  return temp_score     


 
def helper(grid):
    temp_grid_u = copy.deepcopy(grid)
    temp_grid_r = copy.deepcopy(grid)
    temp_grid_d = copy.deepcopy(grid)
    temp_grid_l= copy.deepcopy(grid)
    us=calculate_up(temp_grid_u,2)
    rs=calculate_right(temp_grid_r,2)
    ds=calculate_down(temp_grid_d,2)
    ls=calculate_left(temp_grid_l,2)
    
    if us>=rs and us >=ds and us >=ls:
      return 0
    elif rs>=us and rs>=ds and rs>=ls:
      return 1
    elif ds>=us and ds>=rs and ds>=ls:
      return 2
    else :
      return 3
    


@app.route("/")
def index() -> None:
  grid = list(map(int, request.args.get("state").split(",")))
  print('grid = ',grid)
  grid = [grid[i:i+4] for i in range(0, len(grid), 4)]
  print('grid updated = ',grid)  
  out=helper(grid)
  # use 4x4 grid (col-major) to predict best move (sample move: random)
 
  response = Response(str(out))
  print('response :',response)
  response.headers["access-control-allow-origin"] = "*"
  return response

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
