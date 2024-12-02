import json
from pyrcareworld.envs.bathing_env import BathingEnv
import numpy as np
import cv2
import argparse


def _main(dev):
    '''
    Runs the simulation  to verify the sponge's force values from the Unity executable or editor.
    '''
    # Initialize the environment
    if dev:
        env = BathingEnv(executable_file="@editor", seed=100)
    else:
        env = BathingEnv(seed=100)
    print(env.attrs)

    sponge = env.get_sponge()
    # Teleport sponge onto right thigh for testing.
    sponge.SetPosition(position=[-0.108999997,0.91,0.05])

    # Read collision output.
    for _ in range(9000):
        force = sponge.GetForce()
        env.step()

        print(force)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RCareWorld bathing environment simulation for sponge forces.')
    parser.add_argument('-d', '--dev', action='store_true', help='Run in developer mode')
    args = parser.parse_args()
    _main(args.dev)
