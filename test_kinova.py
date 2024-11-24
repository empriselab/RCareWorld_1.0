from pyrcareworld.envs.base_env import RCareWorld
import math
env = RCareWorld()
env.step()

kinova = env.GetAttr(70902)
gripper = env.GetAttr(709060)
env.step()
# TARGETS #
target0 = env.GetAttr(70800)
target1 = env.GetAttr(70801)
target2 = env.GetAttr(70802)
target3 = env.GetAttr(70803)
targets = []
# END TARGETS #
# GRASP CUBES #
gc0 = env.GetAttr(70700)

for i in range(10000):
    position = gc0.data["position"]
    env.step()
    kinova.IKTargetDoMove(position=position,duration=0,speed_based=False)
    env.step()
