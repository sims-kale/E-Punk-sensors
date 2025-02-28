from controller import Robot, DistanceSensor, Motor

# Constants
TIME_STEP = 32
NB_DIST_SENS = 8
PS_RIGHT_00 = 0
PS_RIGHT_45 = 1
PS_RIGHT_90 = 2
PS_RIGHT_REAR = 3
PS_LEFT_REAR = 4
PS_LEFT_90 = 5
PS_LEFT_45 = 6
PS_LEFT_00 = 7

NB_GROUND_SENS = 3
GS_LEFT = 0
GS_CENTER = 1
GS_RIGHT = 2

PS_OFFSET_SIMULATION = [300] * 8
PS_A = 300
PS_B = 100
PS_C = 80

# Initialize robot
robot = Robot()

# Initialize proximity sensors
ps = []
for i in range(NB_DIST_SENS):
    sensor = robot.getDevice(f'ps{i}')
    sensor.enable(TIME_STEP)
    ps.append(sensor)

# Initialize ground sensors
gs = []
for i in range(NB_GROUND_SENS):
    sensor = robot.getDevice(f'gs{i}')
    sensor.enable(TIME_STEP)
    gs.append(sensor)

# Initialize motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# State variables
ontrack = True
avoiding = False
around = False
recovery = False

# Main loop
while robot.step(TIME_STEP) != -1:
    # Read sensor values
    ps_value = [max(0, int(ps[i].getValue() - PS_OFFSET_SIMULATION[i])) for i in range(NB_DIST_SENS)]
    gs_value = [gs[i].getValue() for i in range(NB_GROUND_SENS)]
    
    # Initialize speeds
    speed_left = 0
    speed_right = 0
    
    # Line Following Module
    if ontrack:
        delta_s = gs_value[GS_RIGHT] - gs_value[GS_LEFT]
        lfm_forward_speed = 200
        lfm_k_gs_speed = 0.4
        speed_left = lfm_forward_speed - lfm_k_gs_speed * delta_s
        speed_right = lfm_forward_speed + lfm_k_gs_speed * delta_s
    
    # Obstacle avoidance logic
    if ps_value[PS_LEFT_00] > PS_A or ps_value[PS_RIGHT_00] > PS_A:
        avoiding = True
    
    if avoiding:
        if ps_value[PS_LEFT_90] < (PS_A - 20):
            speed_left = 200
            speed_right = -200
        elif ps_value[PS_LEFT_90] >= PS_A:
            avoiding = False
            around = True
    
    if around:
        if ps_value[PS_LEFT_90] < (PS_A - 20) and ps_value[PS_LEFT_45] < PS_B:
            speed_left = -200
            speed_right = 100
        if any(v < 400 for v in gs_value):
            around = False
            recovery = True
            ontrack = False
    
    if recovery:
        if ps_value[PS_LEFT_90] > PS_C:
            speed_left = 200
            speed_right = -200
        else:
            recovery = False
            ontrack = True
    
    # Set motor speeds
    left_motor.setVelocity(speed_left * 0.00628)
    right_motor.setVelocity(speed_right * 0.00628)
    
    # Debug output
    print(f"Ontrack: {not (avoiding or around or recovery)}, "
          f"Avoiding: {avoiding}, Around: {around}, Recovery: {recovery}")