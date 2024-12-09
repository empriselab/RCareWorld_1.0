from pyrcareworld.envs.base_env import RCareWorld
import pyrcareworld.attributes as attr

import os
import sys
import argparse
from pyrcareworld.demo import executable_path

def _main(dev):
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
  # Initialize the environment with the specified scene file
  player_path = os.path.join(executable_path, "../executable/Player/Player.x86_64")

  env = RCareWorld(assets=["Collider_Box", "Rigidbody_Sphere"], executable_file="@editor" if dev else player_path)

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
  env.Pend()

  env.SaveScene("test_scene.json")
  env.ClearScene()
  env.Pend()

  env.LoadSceneAsync("test_scene.json")
  env.Pend()
  env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RCareWorld bathing environment simulation for sponge forces.')
    parser.add_argument('-d', '--dev', action='store_true', help='Run in developer mode')
    args = parser.parse_args()
    _main(args.dev)
