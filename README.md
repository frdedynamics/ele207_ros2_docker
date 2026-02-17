# ELE207 ROS2 (Foxy) Docker Container
A ROS2 Foxy Docker container for mobile robotics labs in ELE207.

# Setup Process
* Install [Docker Desktop] (https://docs.docker.com/desktop/). Alternatively if you are using Linux you can only instal [Docker Engine](https://docs.docker.com/engine/install) as well.
* Clone this repository, and in a terminal window navigate to it using the `cd PATH` command. **Note:** `PATH` has to be replaced with an actual path, e.g. `cd C:\Users\max\Desktop\ele207_ros2_docker`.
* Build the docker image: `docker build -t ele207/ros2_env .`

# Usage Instructions
* Run the docker container: `docker run -it --net=host --rm --name ele207_ros2_container ele207/ros2_env`
  **Note:** This will automatically also start the rosboard node to visualize topics. The rosboard can be accessed in a browser window under the following URL: `http://localhost:8888/`
* Opening a terminal window in the docker container: `docker exec -it ele207_ros2_container bash`

# Changing ROS_DOMAIN_ID
To change the ROS_DOMAIN_ID modify line 32 in the **Dockerfile** file. Afterwards you have to rebuild the docker image as described in [Setup Process](#setup-process).

# Running Braitenberg Vehicle Controller
1. SSH into the turtlebot and run `ros2 launch turtlebot3_manipulation_bringup hardware.launch.py`.
2. Open a terminal window and run `docker run -it --net=host --rm --name ele207_ros2_container ele207/ros2_env`
3. Open another terminal window and run `docker exec -it ele207_ros2_container bash`. This will give you access to the terminal inside the Docker container. In the same terminal window run `ros2 run braitenberg_vehicle controller`

# Modifying Controller Code
1. Ctrl+C the terminal window that is running the controller.
2. Use the vscode **Container** extention to modify the controller file located in `ele207/ros2_env/Files/root/ros2_ws/src/braitenberg_vehicle/braitenberg_vehicle/controller.py`. After modification save the file with Ctrl+S.
3. Run the controller using the `ros2 run braitenberg_vehicle controller` command.

