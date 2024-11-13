import pytest
from pyrcareworld.envs.base_env import RCareWorld
import pyrcareworld.attributes as attr
from pyrcareworld.envs.bathing_env import BathingEnv
from pyrcareworld.envs.dressing_env import DressingEnv

import os
import sys

def test_save_dressing():
  # Initialize the environment with the specified scene file
  env = DressingEnv(assets=["Collider_Box", "Rigidbody_Sphere"], graphics=False, log_level=1)

  box1 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box1.SetTransform(position=[-0.5, 0.5, 0], scale=[0.1, 1, 1])
  box2 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box2.SetTransform(position=[0.5, 0.5, 0], scale=[0.1, 1, 1])
  box3 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box3.SetTransform(position=[0, 0.5, 0.5], scale=[1, 1, 0.1])
  box4 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box4.SetTransform(position=[0, 0.5, -0.5], scale=[1, 1, 0.1])
  sphere = env.InstanceObject(name="Rigidbody_Sphere", attr_type=attr.RigidbodyAttr)
  sphere.SetTransform(position=[0, 0.5, 0], scale=[0.5, 0.5, 0.5])
  env.ClearScene()
  env.step(1)
  env.SaveScene("helpme.json")
  env.step(1)
  env.close()

  current_dir = os.getcwd()
  print(f"Current working directory: {current_dir}")
  assert os.path.exists("template/Dressing/DressingPlayer_Data")
  assert os.path.exists("template/Dressing/DressingPlayer_Data/StreamingAssets/SceneData/helpme.json")

def test_save_bathing():
  env = BathingEnv(assets=["Collider_Box", "Rigidbody_Sphere"], graphics=False, log_level=1)

  box1 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box1.SetTransform(position=[-0.5, 0.5, 0], scale=[0.1, 1, 1])
  box2 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box2.SetTransform(position=[0.5, 0.5, 0], scale=[0.1, 1, 1])
  box3 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box3.SetTransform(position=[0, 0.5, 0.5], scale=[1, 1, 0.1])
  box4 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr)
  box4.SetTransform(position=[0, 0.5, -0.5], scale=[1, 1, 0.1])
  sphere = env.InstanceObject(name="Rigidbody_Sphere", attr_type=attr.RigidbodyAttr)
  sphere.SetTransform(position=[0, 0.5, 0], scale=[0.5, 0.5, 0.5])
  env.step(1)
  env.SaveScene("helpme.json")

  # Give some time to save...
  for _ in range(10):
    env.step()

  env.close()

  current_dir = os.getcwd()
  print(f"Current working directory: {current_dir}")
  assert os.path.exists("template/Bathing/BathingPlayer_Data")
  assert os.path.exists("template/Bathing/BathingPlayer_Data/StreamingAssets/SceneData/helpme.json")
