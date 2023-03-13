from pyrcareworld.envs import RCareWorld

env = RCareWorld()
env.create_robot(id = 315893, gripper_list = ['3158930'], robot_name= 'kinova_gen3_7dof-robotiq85', base_pos=[0, 0, 1])
robot = env.get_robot(315893)
env.create_object(id = 315867, name = 'Cube', is_in_scene=True)
cube = env.get_object(315867)
while True:
    position = cube.getPosition()
    print(position)
    robot.directlyMoveTo(position)
    env._step()