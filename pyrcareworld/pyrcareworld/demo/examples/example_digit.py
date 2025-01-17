import os
import sys

# Add the project directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pyrcareworld.envs.base_env import RCareWorld
from pyrcareworld.attributes.digit_attr import DigitAttr

# Initialize the environment
env = RCareWorld()

# Create an instance of a Digit object and set its position
digit = env.InstanceObject(name="Digit", attr_type=DigitAttr)
digit.SetTransform(position=[0, 0.015, 0])

# Create an instance of a target object and set its position
target = env.InstanceObject(name="DigitTarget")
target.SetTransform(position=[0, 0.05, 0.015])

# Set the view transform for the environment
env.SetViewTransform(position=[-0.1, 0.033, 0.014], rotation=[0, 90, 0])

# Perform a simulation step
env.Pend()

# You can then drag the sphere to interact with the digit sensor
# Close the environment
env.close()
