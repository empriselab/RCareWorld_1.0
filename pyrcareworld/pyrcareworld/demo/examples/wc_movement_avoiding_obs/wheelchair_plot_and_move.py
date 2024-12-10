from pyrcareworld.envs.base_env import RCareWorld
import math
import numpy as np
from rrt_algorithms.rrt.rrt import RRT
from rrt_algorithms.search_space.search_space import SearchSpace
from rrt_algorithms.utilities.plotting import Plot

env = RCareWorld()
env.step()

class Wheelchair:
    def __init__(self, wheelchair_id, wheelchair_loc_id):
        '''
        Initializes with wheelchair id and wheelchair_loc_id
        '''
        self.wheelchair = env.GetAttr(wheelchair_id)
        self.wheelchair_loc = env.GetAttr(wheelchair_loc_id)

    def desired_degree(self, object, obj_cur_r, desired_degree):
        '''
        Moves toward the desired angle given the objects current rotation.
        obj_cur_r is the current angle of the object
        desired_degree is the target angle
        '''
        r_change = obj_cur_r - desired_degree
        while r_change < -180:
            r_change += 360
        while r_change > 180:
            r_change -= 360
        if r_change > 0:
            object.TurnLeft(1,1)
            env.step()
        else:
            object.TurnRight(1,1)
            env.step()

    def repeat_til_desired_degree(self,obj,target_r,r_threshold):
        '''
        Will repeatedly move the obj until it hits the angle specified in target_r within the r_threshold
        '''
        obj_r = obj.data["local_rotations"][0][2]   
        while abs(obj_r - target_r) >= r_threshold:
            obj_r = obj.data["local_rotations"][0][2]
            self.desired_degree(obj, obj_r, target_r)
        return

    def traveling_pts(self,targets):
        '''
        targets is the series of waypoints which the wheelchair will visit until the final destination
        '''
        reached_target = True
        current_target_index = -1
        while current_target_index < len(targets):
            if reached_target == True and current_target_index < len(targets) - 1:
                current_target_index += 1
                target = targets[current_target_index]
                obj_pos, target_pos = self.wheelchair_loc.data["position"], target
                new_coords = []
                wc_r = self.wheelchair.data["local_rotations"][0][2]
                new_coords.append(obj_pos[0] - target_pos[0])
                new_coords.append(obj_pos[2] - target_pos[2])
                target_r = math.atan(new_coords[0]/new_coords[1]) * (180 / math.pi)
                if new_coords[1] > 0:
                    target_r -= 180
                if target_r < 0:
                    target_r += 360
                self.repeat_til_desired_degree(self.wheelchair,target_r,1)
                reached_target = False
            if reached_target == True and current_target_index == len(targets) - 1:
                current_target_index += 1
                target_r = 0
                self.repeat_til_desired_degree(self.wheelchair,target_r,1)
            if reached_target == False:
                target = targets[current_target_index]
                wc_pos, target_pos = self.wheelchair_loc.data["position"], target
                wc_r = self.wheelchair.data["local_rotations"][0][2]
                reached_target = self.object_to_target(self.wheelchair, wc_pos, wc_r, target_pos, 1, 0.2)

    

    def object_to_target(self, object, obj_pos, obj_r, target_pos, r_threshold=1, d_threshold=3):
        '''
        object to target will move the object given its current position (obj_pos) rotation (obj_r) and the position of the target.
        '''
        new_coords = []
        new_coords.append(obj_pos[0] - target_pos[0])
        new_coords.append(obj_pos[2] - target_pos[2])
        target_r = math.atan(new_coords[0]/new_coords[1]) * (180 / math.pi)
        if new_coords[1] > 0:
            target_r -= 180
        if target_r < 0:
            target_r += 360
        setreturn = True
        if abs(obj_r - target_r) >= r_threshold:
            self.desired_degree(object, obj_r, target_r)
        if self.distance(obj_pos,target_pos) >= d_threshold:
            object.MoveForward(5,1)
            setreturn = False
            env.step()
        return setreturn

    def distance(self,d1,d2):
        '''
        basic distance function, ignoring the y-axis
        '''
        return math.sqrt((d2[0] - d1[0])**2 + (d2[2] - d1[2])**2)
    
    def rrt_path_plan(self, obs_list_ids, xdim, x_goal, scale=1.7):
        '''
        plan the path given a list of obstacles
        '''
        obstacles = []
        for x in range(len(obs_list_ids)):
            ob = env.GetAttr(obs_list_ids[x])
            obstacles.append(ob)

        start_pos = self.wheelchair_loc.data["position"]
        x_init = (start_pos[0], start_pos[2])

        def setup_obs(obs):
            Obstacles = []
            for x in range(len(obs)):
                ob = obs[x]
                pos_x = ob.data['local_to_world_matrix'][0][3]
                scale_x = ob.data['local_to_world_matrix'][0][0]
                pos_z = ob.data['local_to_world_matrix'][2][3]
                scale_z = ob.data['local_to_world_matrix'][2][2]
                x_lower = pos_x-scale_x/scale
                z_lower = pos_z-scale_z/scale
                x_upper = pos_x+scale_x/scale
                z_upper = pos_z+scale_z/scale
                Obstacles.append((x_lower, z_lower, x_upper, z_upper))
            return np.array(Obstacles, dtype=object)

        Obstacles = setup_obs(obstacles)

        X_dimensions = np.array(xdim) # dimensions of Search Space [(x_lower, x_upper), (y_lower, y_upper), ...]

        q = 1  # length of tree edges
        r = .1  # length of smallest edge to check for intersection with obstacles
        max_samples = 1024  # max number of samples to take before timing out
        prc = 0.1  # probability of checking for a connection to goal

        # create search space
        X = SearchSpace(X_dimensions, Obstacles)

        # create rrt_search
        rrt = RRT(X, q, x_init, x_goal, max_samples, r, prc)
        path = rrt.rrt_search()

        reg_path = [(float(x), 0, float(y)) for x, y in path]
        reg_path = reg_path[1:]

        # plot
        plot = Plot("rrt_2d")
        plot.plot_tree(X, rrt.trees)
        if path is not None:
            plot.plot_path(X, path)
        plot.plot_obstacles(X, Obstacles)
        plot.plot_start(X, x_init)
        plot.plot_goal(X, x_goal)
        plot.draw(auto_open=True)

        return reg_path

wc = Wheelchair(70900,709005)
env.step(10)
reg_path = wc.rrt_path_plan([70600,70601],[(-5, 15), (-15, 5)],(4.989, -3.839))
env.step(10)
wc.traveling_pts(reg_path)

while 1:
    env.step()