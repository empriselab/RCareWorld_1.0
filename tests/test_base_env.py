import pytest
from pyrcareworld.envs.base_env import RCareWorld
import pyrcareworld.attributes as attr
from pyrcareworld.envs.bathing_env import BathingEnv
from pyrcareworld.envs.dressing_env import DressingEnv

import os
import sys

from pyrcareworld.demo import urdf_path
from pyrcareworld.demo import executable_path
from pyrcareworld.demo import mesh_path

def test_save_and_load():
  player_path = "pyrcareworld/pyrcareworld/demo/executable/Player/Player.x86_64"

  env = RCareWorld(assets=["Collider_Box", "Rigidbody_Sphere"], executable_file=player_path, graphics=False)

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

  env.SaveScene("test_scene.json")

  # Give some time to save...
  for _ in range(10):
    env.step()

  assert env.GetAttr(1).data["name"] == "Collider_Box"
  assert env.GetAttr(2).data["name"] == "Collider_Box"
  assert env.GetAttr(3).data["name"] == "Collider_Box"
  assert env.GetAttr(4).data["name"] == "Collider_Box"
  assert env.GetAttr(5).data["name"] == "Rigidbody_Sphere"

  assert os.path.exists("pyrcareworld/pyrcareworld/demo/executable/Player/Player_Data/StreamingAssets/SceneData/test_scene.json")

  env.ClearScene()

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

  # Give some time to load...
  for _ in range(10):
    env.step()

  assert env.GetAttr(1).data["name"] == "Collider_Box"
  assert env.GetAttr(2).data["name"] == "Collider_Box"
  assert env.GetAttr(3).data["name"] == "Collider_Box"
  assert env.GetAttr(4).data["name"] == "Collider_Box"
  assert env.GetAttr(5).data["name"] == "Rigidbody_Sphere"

  env.close()

def test_object_listener():
  env = RCareWorld(assets=["CustomAttr"], executable_file="pyrcareworld/pyrcareworld/demo/executable/Player/Player.x86_64", graphics=False)

  called = False

  custom = env.InstanceObject(name="CustomAttr", id=1, attr_type=attr.CustomAttr)

  def object_listener(args):
      nonlocal called
      called = True
      dict = {}
      for i, arg in enumerate(args):
          dict[i] = arg
          print(i, arg, type(arg))

      assert dict[0] == "string:"
      assert dict[1] == "This is dynamic object"
      assert dict[2] == "int:"
      assert dict[3] == 123
      assert dict[4] == "float:"
      assert dict[5] == float(456.0)
      assert dict[6] == "bool:"
      assert dict[7] == False
      assert dict[8] == "list:"
      assert str(dict[9]) == "[7.889999866485596, 1.1100000143051147]"
      assert dict[10] == "dict:"
      assert str(dict[11]) == "{'a': 1, 'b': 2}"
      assert dict[12] == "tuple:"
      assert str(dict[13]) == "('a', 1, 0.5619999766349792)"
  
  env.AddListenerObject("DynamicObject", object_listener)

  env.SendObject(
      "DynamicObject",
      "string:", "this is dynamic object",
      "int:", 1,
      "bool:", True,
      "float:", 4849.6564,
      "list:", [616445.085, 9489984.0, 65419596.0, 9849849.0],
      "dict:", {"1": 1, "2": 2, "3": 3},
      "tuple:", ("1", 1, 0.562)
  )

  # Get data back...
  env.step(10)
  assert called

  env.close()

def test_load_objects():
  env = RCareWorld(assets=["CustomAttr"], executable_file="pyrcareworld/pyrcareworld/demo/executable/Player/Player.x86_64", graphics=False)

  robot = env.LoadURDF(
    path=os.path.join(urdf_path, "UR5/ur5_robot.urdf"),
    native_ik=False,
    id=1
  )

  mesh = env.LoadMesh(
    path=os.path.join(mesh_path, "002_master_chef_can/google_16k/textured.obj",),
    id=2
  )

  t_shirt_path = os.path.join(mesh_path, 'Tshirt.obj')
  cloth = env.LoadCloth(path=t_shirt_path, id=3)

  env.step(3)

  assert env.GetAttr(1) == robot
  assert env.GetAttr(2) == mesh
  assert env.GetAttr(3) == cloth

  env.close()


# TODO: Test more functions of the environment
