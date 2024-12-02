import json
from pyrcareworld.envs.bathing_env import BathingEnv
import numpy as np
import cv2
import argparse


def _main(dev):
    '''
    Runs the simulation to allow a developer to verify the grasp point position is being read from the Unity executable or editor.
    '''
    # Initialize the environment
    if dev:
        env = BathingEnv(executable_file="@editor", seed=100)
    else:
        env = BathingEnv(seed=100)
    print(env.attrs)

    robot = env.get_robot()
    position1 = (0.492, 0.644, 0.03)

    robot.IKTargetDoMove(
        position=[position1[0], position1[1] + 0.5, position1[2]],
        duration=2,
        speed_based=False,
    )
    robot.WaitDo()
    robot.IKTargetDoMove(
        position=[position1[0], position1[1], position1[2]],
        duration=2,
        speed_based=False,
    )
    robot.WaitDo()
    robot.IKTargetDoKill()

    # Read collision output.
    for _ in range(9000):
        pos, rot = robot.GetGraspPoint(euler=True)
        env.step()

        print(pos, rot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RCareWorld bathing environment simulation for grasp point position.')
    parser.add_argument('-d', '--dev', action='store_true', help='Run in developer mode')
    args = parser.parse_args()
    _main(args.dev)
