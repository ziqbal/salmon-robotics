
from threading import Thread

import os
import sys
import signal
import time

import websocket
import threading
import random

import scratch

import logging

logging.basicConfig( )

###############################################################

_power_left = "*"
_power_right= "*"
_encoder_left = "*"
_encoder_right= "*"
_angle = "*"
_distance_min = "*"
_distance_max = "*"
_timer_left = "*"
_timer_right = "*"

###############################################################

def on_message( ws , message ) :

  global monitoring
  global sc

  if( message.strip( ) == "" ) : return

  print( str( int( round( time.time( ) * 1000 ) ) ) + "," + message )

  parts = message.split( "," )

  if( len( parts ) == 6 and parts[ 1 ] == "_" ) :

    encoder1_count = int( parts[ 2 ] )
    encoder2_count = int( parts[ 3 ] )
    imu_gyro_z = float( parts[ 4 ] )
    distance_range = int( parts[ 5 ] )

    sc.sensorupdate( { "motor_right" : encoder1_count , "motor_left" : encoder2_count , "angle" : imu_gyro_z , "range" : distance_range } )
    sc.broadcast( "_updated" )

def on_close( ws ) :

  print( "### closed ###" )

def on_error( ws , error ) :
    
    print( error )

##############################################################################
#websocket.enableTrace(True)
ws = websocket.WebSocketApp( "ws://mightymouse.local/ws", on_message = on_message , on_close = on_close ,on_error=on_error)
#ws = websocket.WebSocketApp( "ws://192.168.1.12/ws", on_message = on_message , on_close = on_close ,on_error=on_error)
wst = threading.Thread( target = ws.run_forever )
wst.daemon = True
wst.start( )
##############################################################################

conn_timeout = 5

while not ws.sock.connected and conn_timeout :

  time.sleep( 1 )
  conn_timeout -= 1
  if( conn_timeout == 0 ) : print( "conn_timeout...?" )

print( "WS connected" )

##############################################################################
sc = scratch.Scratch( )

def listen( ) :

  while True:
    try :

      yield sc.receive( )

    except scratch.ScratchError :
      
      raise StopIteration

##############################################################################


from threading import Thread

def myfunc(i):
  global sc
  while True:
    print(".")
    if(not sc.connected):
      print("exit")
      os.kill(os.getpid(), signal.SIGINT)
      return
    time.sleep(3)

t = Thread(target=myfunc, args=(0,))
t.daemon = True
t.start()

###

flag_sensor_update = True

while ws.sock.connected :

  for msg in listen( ) :

    print( msg )

    if msg[ 0 ] == "broadcast" :

      if( msg[ 1 ] == "_init" ) :
        _power_left = "*"
        _power_right = "*"
        _encoder_left = "*"
        _encoder_right = "*"
        _angle = "*"
        _distance_min = "*"
        _distance_max = "*"
        _timer_left = "*"
        _timer_right = "*"
        continue

      if( msg[ 1 ] == "_monitor_on" ) :
        ws.send( msg[ 1 ] )
        continue
      if( msg[ 1 ] == "_monitor_off" ) :
        ws.send( msg[ 1 ] )
        continue

      if( msg[ 1 ] == "_origin" ) :
        ws.send( "O" )
        continue

      if( msg[ 1 ] == "_scan" ) :
        ws.send( "S" )
        continue

      if( msg[ 1 ] == "_monitor" ) :
        ws.send( "M" )
        continue

      if( msg[ 1 ] == "_go" ) :
        power_str = str( _power_left ) + "," + str( _power_right )
        encoder_str = str( _encoder_left ) + "," + str( _encoder_right )
        angle_str = str( _angle ) 
        distance_str = str( _distance_min ) + "," + str( _distance_max )
        timer_str = str( _timer_left ) + "," + str( _timer_right )

        msg_str = ">," + power_str + "," + encoder_str + "," + angle_str + "," + distance_str + "," + timer_str 
        print(msg_str)
        ws.send( msg_str )

        #sc.sensorupdate( { "_power_left" : "*" , "_power_right" : "*" , "_angle" : "*" , "_distance_min" : "*" , "_distance_max" : "*" , "_timer_left" : "*" , "_timer_right" : "*" } )

        continue

      continue

    if( msg[ 0 ] == "sensor-update" ) :

      if( flag_sensor_update ) :
        flag_sensor_update = False
        continue

      for k , v in msg[ 1 ].items( ) :

        if( k[ 0 ] != "_" ) : continue

        if( k == "_power_left" ) :
          _power_left = v
          continue
        if( k == "_power_right" ) :
          _power_right= v
          continue
        if( k == "_encoder_right" ) :
          _encoder_right= v
          continue
        if( k == "_encoder_left" ) :
          _encoder_left= v
          continue

        if( k == "_angle" ) :
          _angle = v
          continue

        if( k == "_distance_min" ) :
          _distance_min = v
          continue
        if( k == "_distance_max" ) :
          _distance_max = v
          continue

        if( k == "_timer_left" ) :
          _timer_left = v
          continue
        if( k == "_timer_right" ) :
          _timer_right = v
          continue

      continue

    time.sleep( 0.01 )
  time.sleep( 0.01 )
