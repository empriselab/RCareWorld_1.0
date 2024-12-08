"""Tests for the bathing environment.

NOTE: run this file with pytest -s tests/test_bathing_env.py.
"""

from pyrcareworld.attributes.camera_attr import CameraAttr
from pyrcareworld.envs.bathing_env import BathingEnv

import pytest
import numpy as np

from .test_angle_functions import euler_angles_allclose


@pytest.fixture(scope="session", name="bathing_env", autouse=True)
def _bathing_env_fixture():
    """Create a BathingEnv once and share it across tests."""
    # NOTE: set graphics = True here to debug.
    env = BathingEnv(graphics=False, log_level=1)    
    yield env
    env.close()


def test_bathing_stretch_move_commands(bathing_env: BathingEnv):
    """Tests for turning and moving the stretch base in the bathing env."""

    num_steps_per_command = 300
    robot = bathing_env.get_robot()

    # Move forward.
    robot_base_position = robot.data["positions"][0].copy()
    robot.MoveForward(0.5, 0.5)
    bathing_env.step(num_steps_per_command)
    new_robot_base_position = robot.data["positions"][0].copy()
    expected_robot_base_position = np.add(robot_base_position, (0, 0, 0.5))
    # NOTE: moving is not precise beyond ~0.25. Users may want to build a controller
    # on top to compensate.
    assert np.allclose(new_robot_base_position, expected_robot_base_position, atol=0.25)

    # Move backward.
    robot_base_position = robot.data["positions"][0].copy()
    robot.MoveBack(0.5, 0.5)
    bathing_env.step(num_steps_per_command)
    new_robot_base_position = robot.data["positions"][0].copy()
    expected_robot_base_position = np.add(robot_base_position, (0, 0, -0.5))
    assert np.allclose(new_robot_base_position, expected_robot_base_position, atol=0.25)

    # Turn left.
    robot_base_rotation = robot.data["rotations"][0].copy()
    robot.TurnLeft(90, 1)  # turn the robot left 90 degrees with a speed of 1.
    bathing_env.step(num_steps_per_command)  # long enough for the full turn
    # The yaw should have changed by about 90 degrees.
    new_robot_base_rotation = robot.data["rotations"][0].copy()
    expected_robot_base_rotation = np.add(robot_base_rotation, (0.0, -90.0, 0))
    # NOTE: turning is not precise beyond ~5 degrees. Users may want to build a controller
    # on top to compensate.
    assert euler_angles_allclose(new_robot_base_rotation, expected_robot_base_rotation, atol=5.0)

    # Turn right.
    robot_base_rotation = robot.data["rotations"][0].copy()
    robot.TurnRight(90, 1)
    bathing_env.step(num_steps_per_command)
    new_robot_base_rotation = robot.data["rotations"][0].copy()
    expected_robot_base_rotation = np.add(robot_base_rotation, (0.0, 90.0, 0))
    assert euler_angles_allclose(new_robot_base_rotation, expected_robot_base_rotation, atol=5.0)

def test_bathing_collision(bathing_env: BathingEnv):
    """
    Test for collision detection using GetCurrentCollisionPairs in the bathing env.
    """

    num_steps_per_command = 500
    robot = bathing_env.get_robot()

    # Drive against bed.
    robot.MoveBack(6, 0.5)

    bathing_env.step(num_steps_per_command)

    bathing_env.GetCurrentCollisionPairs()
    bathing_env.step()
    assert len(bathing_env.data["collision_pairs"]) > 0
    assert 221582 in bathing_env.data["collision_pairs"][0]
    assert 758554 in bathing_env.data["collision_pairs"][0]
    
    # Drive against drawer.
    robot.MoveForward(6, 0.5)

    bathing_env.step(num_steps_per_command)

    bathing_env.GetCurrentCollisionPairs()
    bathing_env.step()
    assert len(bathing_env.data["collision_pairs"]) > 0 
    assert 221582 in bathing_env.data["collision_pairs"][0]
    assert 758666 in bathing_env.data["collision_pairs"][0]

    # Drive away from drawer.
    robot.MoveBack(0.5, 0.5)

    bathing_env.step(num_steps_per_command)

    bathing_env.GetCurrentCollisionPairs()
    bathing_env.step()
    assert len(bathing_env.data["collision_pairs"]) == 0

@pytest.mark.repeat(3)
def test_seed():
    """Test for the seed."""

    env = BathingEnv(graphics=False, seed=100)    

    env.step(300)

    personCollider = env.GetAttr(env._person_id)
    assert np.allclose(personCollider.data['position'], [-0.703722656,1.19400001,-0.026099354], atol=1e-4)

def test_target_angle_drive(bathing_env: BathingEnv):
    """Tests for movement using `.TargetVelocity()` on the robot."""

    robot = bathing_env.get_robot()
    num_steps_per_command = 300

    # Drive forward by setting left and right velocities.
    robot_base_position = robot.data["positions"][0].copy()
    for _ in range(num_steps_per_command):
        robot.TargetVelocity(0.5, 0.5)
        bathing_env.step()

    new_robot_base_position = robot.data["positions"][0].copy()
    # Hits the drawer.
    expected_robot_base_position = np.add(robot_base_position, (0, 0, 0.51))
    assert np.allclose(new_robot_base_position, expected_robot_base_position, atol=0.03)

    # Drive backward by setting left and right velocities.
    robot_base_position = robot.data["positions"][0].copy()
    for _ in range(num_steps_per_command):
        robot.TargetVelocity(-0.5, -0.5)
        bathing_env.step()

    new_robot_base_position = robot.data["positions"][0].copy()
    # Hits the bed.
    expected_robot_base_position = np.add(robot_base_position, (0, 0, -1.08))
    assert np.allclose(new_robot_base_position, expected_robot_base_position, atol=0.1)

def test_target_angle_turn(bathing_env: BathingEnv):
    robot = bathing_env.get_robot()
    num_steps_per_command = 300

    # Drive left by setting left and right velocities.
    robot_base_rotation = robot.data["rotations"][0].copy()
    for _ in range(num_steps_per_command):
        robot.TargetVelocity(-0.25, 0.25)
        bathing_env.step()

    new_robot_base_rotation = robot.data["rotations"][0].copy()
    expected_robot_base_rotation = np.add(robot_base_rotation, (0, -40, 0))
    assert euler_angles_allclose(new_robot_base_rotation, expected_robot_base_rotation, atol=10.0)

    # Stop for a moment.
    robot.TargetVelocity(0, 0)
    bathing_env.step()

    # Drive right by setting left and right velocities.
    robot_base_rotation = robot.data["rotations"][0].copy()
    for _ in range(num_steps_per_command):
        robot.TargetVelocity(0.25, -0.25)
        bathing_env.step()

    new_robot_base_rotation = robot.data["rotations"][0].copy()
    expected_robot_base_rotation = np.add(robot_base_rotation, (0, 40, 0))
    assert euler_angles_allclose(new_robot_base_rotation, expected_robot_base_rotation, atol=10.0)

def test_joint_names(bathing_env: BathingEnv):
    robot = bathing_env.get_robot()

    bathing_env.step()

    assert "base_link" in robot.data["names"]
    assert "link_left_wheel" in robot.data["names"]
    assert "link_right_wheel" in robot.data["names"]
    assert "link_mast" in robot.data["names"]
    assert "link_lift" in robot.data["names"]

    bathing_env.step()

def test_instance_camera(bathing_env: BathingEnv):
    new_cam: CameraAttr = bathing_env.InstanceObject(name="Camera", id=123456, attr_type=CameraAttr)
    new_cam.SetTransform(position=[0, 1.7, 0], rotation=[90, 0, 0])

    for _ in range(3):
        new_cam.GetRGB(512, 512)
        bathing_env.step()
        rgb = np.frombuffer(new_cam.data["rgb"], dtype=np.uint8)
        print(rgb.shape)
        assert(rgb.shape[0] > 0)

def test_sponge_force():
    """
    Test for the sponge force. Teleports the sponge to the right thigh and reads the force.
    """
    # Stable seed so that the test is consistent.
    env = BathingEnv(graphics=False, seed=100)

    sponge = env.get_sponge()
    assert sponge.GetForce() == [0.0]

    # Teleport sponge onto right thigh for testing.
    sponge.SetPosition(position=[-0.108999997,0.91,0.05])

    # Wait a bit.
    env.step(30)

    # Read collision output.
    for i in range(20):
        force = sponge.GetForce()
        env.step()

        assert force[0] > 0, f"On iteration {i}, force was {force} but should be > 0"

    # Teleport away.
    sponge.SetPosition(position=[-0.108999997,0.532999992,2.227])

    # Wait a bit. Takes a little while for force to zero out.
    for _ in range(40):
        sponge.GetForce()
        env.step()

    # Read collision output.
    for i in range(20):
        force = sponge.GetForce()
        env.step()

        assert force[0] == 0.0, f"On iteration {i}, force was {force} but should be 0"
    
def test_grasp_point_position(bathing_env: BathingEnv):
    """
    Test for the grasp point position and rotation being read correctly.
    """
    robot = bathing_env.get_robot()

    start_pos1 = [0.5203691124916077, 0.25160324573516846, 1.360432744026184]
    start_pos2 = [0.5636255145072937, 0.2514449656009674, 0.8926234245300293]
    start_rot1 = [0.00018492204253561795, 90.03585052490234, 359.6820373535156]
    start_rot2 = [359.94793701171875, 103.28073120117188, 357.9418640136719]

    # A few preemptive calls just in case grasp point not initialized.
    for _ in range(10):
        robot.GetGraspPoint()
        bathing_env.step()

    for _ in range(10):
        pos, rot = robot.GetGraspPoint(euler=True)
        bathing_env.step()

        assert np.allclose(pos, start_pos1, atol=0.1) or np.allclose(pos, start_pos2, atol=0.1)
        assert euler_angles_allclose(rot, start_rot1, atol=5) or euler_angles_allclose(rot, start_rot2, atol=5)

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

    bathing_env.step(5)

    for _ in range(10):
        pos, rot = robot.GetGraspPoint(euler=True)
        bathing_env.step()

        assert not (np.allclose(pos, start_pos1, atol=0.1) or np.allclose(pos, start_pos2, atol=0.1))
        assert not (euler_angles_allclose(rot, start_rot1, atol=5) or euler_angles_allclose(rot, start_rot2, atol=5))
    