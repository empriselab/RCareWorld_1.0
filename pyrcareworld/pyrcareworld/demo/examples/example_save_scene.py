from pyrcareworld.envs.base_env import RCareWorld
import pyrcareworld.attributes as attr

import os
import sys
import argparse
import pytest
from pyrcareworld.demo import executable_path

def _main(dev):
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
  # Initialize the environment with the specified scene file
  player_path = os.path.join(executable_path, "../executable/Player/Player.x86_64")

  env = RCareWorld(assets=["Collider_Box", "Rigidbody_Sphere"], executable_file="@editor" if dev else player_path)

  box1 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr, id=1)
  box1.SetTransform(position=[-0.5, 0.5, 0], scale=[0.1, 1, 1])
  box2 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr, id=2)
  box2.SetTransform(position=[0.5, 0.5, 0], scale=[0.1, 1, 1])
  box3 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr, id=3)
  box3.SetTransform(position=[0, 0.5, 0.5], scale=[1, 1, 0.1])
  box4 = env.InstanceObject(name="Collider_Box", attr_type=attr.ColliderAttr, id=4)
  box4.SetTransform(position=[0, 0.5, -0.5], scale=[1, 1, 0.1])
  sphere = env.InstanceObject(name="Rigidbody_Sphere", attr_type=attr.RigidbodyAttr, id=5)
  sphere.SetTransform(position=[0, 0.5, 0], scale=[0.5, 0.5, 0.5])
  env.Pend()

  env.SaveScene("test_scene.json")
  env.ClearScene()
  env.Pend()

  with pytest.raises(AssertionError):
    env.GetAttr(1)

  with pytest.raises(AssertionError):
    env.GetAttr(2)

  with pytest.raises(AssertionError):
    env.GetAttr(3)

  with pytest.raises(AssertionError):
    env.GetAttr(4)

  with pytest.raises(AssertionError):
    env.GetAttr(5)

  env.LoadSceneAsync("test_scene.json")
  env.Pend()

  assert env.GetAttr(1).data["name"] == "Collider_Box"
  assert env.GetAttr(2).data["name"] == "Collider_Box"
  assert env.GetAttr(3).data["name"] == "Collider_Box"
  assert env.GetAttr(4).data["name"] == "Collider_Box"
  assert env.GetAttr(5).data["name"] == "Rigidbody_Sphere"

  env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RCareWorld bathing environment simulation for sponge forces.')
    parser.add_argument('-d', '--dev', action='store_true', help='Run in developer mode')
    args = parser.parse_args()
    _main(args.dev)
