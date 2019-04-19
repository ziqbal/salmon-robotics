import websocket
import time
import random
 
ws = websocket.WebSocket( )
ws.connect( "ws://mightymouse.local/ws" )

print( "connected" ) 

time.sleep( 1 )

print( "origin" )
ws.send( "O" )
time.sleep( 1 )

# power_left power_right encoder_left encoder_right angle distance_min distance_max timer_left timer_right

#584469,_trigger,5
#584514,_,-355,339,361.02,9999
#584562,_,-355,339,360.88,9999

def scan_closest( ) :
  ws.send( "S" )
  while True :
    result = ws.recv( )
    parts=result.split( "," )
    if( len( parts ) == 3 and parts[ 1 ] == "S" ) :
      print(parts)
      break



def scan_distance( ) :
  ws.send( ">,55,55,*,*,*,150,*,*,*" )
  while True:
    result = ws.recv( )
    print("A"+result) 
    parts=result.split(",")
    if(len(parts)==3 and parts[1]=="T"):
      break
  ws.send( ">,-55,-55,*,*,*,*,160,*,*" )
  while True:
    result = ws.recv( )
    print("B"+result) 
    parts=result.split(",")
    if(len(parts)==3 and parts[1]=="T"):
      break


while True :
  ws.send( "O" )
  #time.sleep( 1 )
  scan_closest( )
  scan_distance( )

  ws.send( ">,55,-55,*,*,60,*,*,*,*" )
  while True:
    result = ws.recv( )
    print(result) 
    parts=result.split(",")
    if(len(parts)==3 and parts[1]=="T"):
      break
  ws.send( ">,50,50,150,*,*,100,*,*,*" )
  while True:
    result = ws.recv( )
    print(result) 
    parts=result.split(",")
    if(len(parts)==3 and parts[1]=="T"):
      break





ws.close( )
exit

