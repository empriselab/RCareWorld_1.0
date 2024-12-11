
from pyrcareworld.envs.base_env import RCareWorld
from pyrcareworld.demo import urdf_path
from pyrcareworld.demo import mesh_path
import os

env = RCareWorld(executable_file="@editor", graphics=False)

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
