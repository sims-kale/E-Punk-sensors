"""obstacle_avoidance controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()
MAX_SPEED = 4.50


# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
LEFT_WHEEL = robot.getDevice('left wheel motor')
RIGHT_WHEEL = robot.getDevice('right wheel motor')
 # Set PositionSensor
LEFT_WHEEL.setPosition(float('inf'))
RIGHT_WHEEL.setPosition(float('inf'))
 # Set Velocity
LEFT_WHEEL.setVelocity(0.5 * MAX_SPEED)
RIGHT_WHEEL.setVelocity(0.5 * MAX_SPEED)

left_sensor= robot.getDevice('gs0')
left_sensor.enable(timestep)
right_sensor = robot.getDevice('gs1')
right_sensor.enable(timestep)

ps = []
ps_list = ['ps0','ps1','ps2','ps3','ps4','ps5','ps6','ps7']
for i in range(0, len(ps_list)):
    ps.append(robot.getDevice(ps_list[i]))
    ps[i].enable(timestep)
    # print(type(ps[i]))
    # print(ps[i])
    
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    value1= left_sensor.getValue()
    value2 = right_sensor.getValue()
    print(f'Left:{value1} | Right:{value2}')
    # THRESHOLD = (max(value1, value2) + min(value1, value2)) / 2
    psValues = []
    for i in range(8):
        val = psValues.append(ps[i].getValue())
       # print('ps[i] :', type(val))
       
    right_obstacle = psValues[0] > 200.0 or psValues[1] > 200.0 or psValues[2] > 200.0
    left_obstacle = psValues[5] > 200.0 or psValues[6] > 200.0 or psValues[7] > 200.0
   
    if value1 >350:
        left = "White"
    else:
        left = "Black"
    if value2 >350:
        right = "White"
    else:
        right = "Black"
    
    if left== "Black" and right =="Black" and not (left_obstacle or right_obstacle):
        LEFT_WHEEL.setVelocity(0.5 * MAX_SPEED)
        RIGHT_WHEEL.setVelocity(0.5 * MAX_SPEED)
        
        
    # if obstacle present move backword
    elif left== "Black" and right =="Black" and (left_obstacle or right_obstacle):
        # LEFT_WHEEL.setVelocity(-0.5 * MAX_SPEED)
        # RIGHT_WHEEL.setVelocity(-0.5 * MAX_SPEED)
        
        LEFT_WHEEL.setVelocity(0.5 * MAX_SPEED)
        RIGHT_WHEEL.setVelocity(-0.5  * MAX_SPEED)
        robot.step(2000) 
        
    elif left == "White" and right == "Black":
        LEFT_WHEEL.setVelocity(0.5* MAX_SPEED)
        RIGHT_WHEEL.setVelocity(-0.5* MAX_SPEED)
    # else left =="White" and right == "Black":
       
    elif left == "Black" and right == "White":
        LEFT_WHEEL.setVelocity(-0.5* MAX_SPEED)
        RIGHT_WHEEL.setVelocity(0.5* MAX_SPEED)
    
    else:
        LEFT_WHEEL.setVelocity(0.0)
        RIGHT_WHEEL.setVelocity(0.0)
        
   
    
    
    # LEFT_WHEEL.setVelocity(0.5 * MAX_SPEED)
    # RIGHT_WHEEL.setVelocity(0.5 * MAX_SPEED)
    # if left_obstacle:
        # turn right
        # LEFT_WHEEL.setVelocity(0.5 * MAX_SPEED)
        # RIGHT_WHEEL.setVelocity(0.5 * MAX_SPEED)
    # elif right_obstacle:
        # turn left
        # LEFT_WHEEL.setVelocity(0.5 * MAX_SPEED)
        # RIGHT_WHEEL.setVelocity(0.5 * MAX_SPEED)



