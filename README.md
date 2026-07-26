# PatrolBot ROS 2 Navigation Workspace

A comprehensive ROS 2 Jazzy and Gazebo Harmonic simulation workspace featuring a custom differential-drive mobile robot configured for automated indoor mapping, localization, and navigation workflows.

---

## 🤖 Robot Specifications 

### Design View (CAD Model) 
<img width="395" height="300" alt="Screenshot 2026-07-26 110434" src="https://github.com/user-attachments/assets/71bb9c2b-6623-4cf7-84c7-9ca8c18ef0be" />


### Gazebo Sim View
<img width="395" height="250" alt="Screenshot from 2026-07-26 10-40-49" src="https://github.com/user-attachments/assets/1241f3ba-c5f5-4839-aafc-a67f05a29c49" />


### Short Description
**PatrolBot** is an agile, multi-wheeled differential-drive autonomous mobile robot framework designed for mapping and autonomous navigation . It consists of only lidar as of now and further sensors will
be added in the future for tasks like vision based tasks and navigation.


---

## 📦 Repository Structure

* **`patrolbot_description/`**: Holds the primary `.xacro` unified robot descriptions, geometric link meshes (`.stl`), parameter configurations, and primary simulation launch scripts.
* **`patrolbot_nav2_bt/`**: Contains customized XML navigation behavior trees mapped out with structured path recovery and adaptive replanning sub-nodes. Includes the progress checker and goal checker to the tree under `FollowPath` so it uses the goal checker and progress checker defined in `nav2_params.yaml`.

```text

├── patrolbot_description
│   ├── config
│   │   ├── amcl_params.yaml
│   │   ├── nav2_params.yaml
│   │   ├── ros_gz_bridge_gazebo.yaml
│   │   └── slam_toolbox_async.yaml
│   ├── launch
│   │   ├── amcl.launch.py
│   │   ├── display.launch.py
│   │   ├── gazebo.launch.py
│   │   ├── nav2.launch.py
│   │   └── slam.launch.py
│   ├── maps
│   │   ├── patrolbot_map.pgm
│   │   └── patrolbot_map.yaml
│   ├── meshes
│   │   ├── base_link.stl
│   │   ├── left_wheel_1.stl
│   │   ├── lidar_1.stl
│   │   └── right_wheel_1.stl
│   ├── package.xml
│   ├── patrolbot_description
│   │   └── __init__.py
│   ├── resource
│   │   └── patrolbot_description
│   ├── rviz
│   │   ├── display.rviz
│   │   ├── gazebo.rviz
│   │   ├── nav2.rviz
│   │   └── slam.rviz
│   ├── setup.cfg
│   ├── setup.py
│   ├── test
│   │   ├── test_copyright.py
│   │   ├── test_flake8.py
│   │   └── test_pep257.py
│   ├── urdf
│   │   ├── materials.xacro
│   │   ├── patrolbot.gazebo
│   │   ├── patrolbot.ros2control
│   │   └── patrolbot.xacro
│   └── worlds
│       └── obstacles.sdf
└── patrolbot_nav2_bt
    ├── behaviour_trees
    │   ├── navigate_through_poses_w_replanning_and_recovery.xml
    │   └── navigate_to_pose_w_replanning_and_recovery.xml
    ├── package.xml
    ├── patrolbot_nav2_bt
    │   └── __init__.py
    ├── resource
    │   └── patrolbot_nav2_bt
    ├── setup.cfg
    ├── setup.py
    └── test
        ├── test_copyright.py
        ├── test_flake8.py
        └── test_pep257.py
```
---

## 🚀 Execution & Deployment Guide (Multi-Terminal Bringup)

Follow these steps across separate terminal tabs to initialize the complete localization and mapping system environment.

### 🏠 Prerequisites & Workspace Setup
Ensure your system paths are built and cleanly sourced inside your workspace root folder before launching:
```bash
colcon build --symlink-install
source install/setup.bash
```

---

### 🖥️ Terminal 1: Launch Gazebo Harmonic Simulation Environment
Spawns the `patrolbot` model into the dynamic tracking workspace and initializes the joint state transforms.
```bash
ros2 launch patrolbot_description gazebo.launch.py
```

### 🖥️ Terminal 2: Initialize Adaptive Monte Carlo Localization (AMCL) & RViz2
Loads your configured map server parameters (`patrolbot_map.yaml`) and opens the RViz layout to track positioning states.
```bash
ros2 launch patrolbot_description amcl.launch.py
```

### 🖥️ Terminal 3: Execute Navigation2 (Nav2) Path Planning System
Triggers the behavior tree execution engines to read laser scans and receive 2D Navigation Goal pointers from the interface.
```bash
ros2 launch patrolbot_description nav2.launch.py
```

---

## SLAM Toolbox & Navigation Demonstrations

### Simultaneous Localization and Mapping (SLAM Toolbox)
Below is a demonstration of real-time 2D environment mapping using laser rangefinders and odometry processing frames:


https://github.com/user-attachments/assets/0932c142-406e-4557-85cf-c606c050ada9










### Autonomous Nav2 Path Planning & Obstacle Recovery
Watch the navigation engine calculate smooth trajectories, avoid dynamic objects, and utilize behavior trees to recover paths:
Controller used here is DWB as the primary one and Rotation Shim controller takes control when patrolbot rotates to goal.


https://github.com/user-attachments/assets/191b9b4b-b8a2-4f40-80b5-7d80ae5ac5f8




