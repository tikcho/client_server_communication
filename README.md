# ROSclinet_server_communication

Server is located in matlap_server.py (https://github.com/Aimi-no/MatlabRunningServer) and matlap_server_img.py (for images) and an example sending a request is in ros_server_communication folder in test_communication.py. 

Change the URL in the in test_communication.py file to the IP running on your server.

Run example: 
python matlab_server_img.py  --matlab_path "/usr/local/MATLAB/R2020b/bin/matlab" --matlab_script_folder /<path to test.m> --matlab_function test

Run test example in python from ROS workspace: 
rosrun ros_server_communication test_communication.py
