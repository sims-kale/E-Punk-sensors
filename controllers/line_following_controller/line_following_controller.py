"""line_following_controller controller."""
from controller import Robot, Motor
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
robot = Robot()
time_speed = 50
max_speed = 4.50

# Get the time step of the current world
TIME_STEP = int(robot.getBasicTimeStep())

# Get the motors
leftWheel = robot.getDevice("left wheel motor")
rightWheel = robot.getDevice("right wheel motor")

# Set motors to infinite rotation
leftWheel.setPosition(float('inf'))
rightWheel.setPosition(float('inf'))

# Set initial velocity
leftWheel.setVelocity(0.1 * max_speed)
rightWheel.setVelocity(0.1 * max_speed)

# Get and enable sensors
left_gs0 = robot.getDevice('gs0')
right_gs1 = robot.getDevice('gs2')
left_gs0.enable(TIME_STEP)
right_gs1.enable(TIME_STEP)

# Main loop
while robot.step(TIME_STEP) != -1:
    val1 = left_gs0.getValue()
    val2 = right_gs1.getValue()

    print("Value 1:", val1)
    print("Value 2:", val2)

# Enter here exit cleanup code.
