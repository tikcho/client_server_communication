#!/usr/bin/env python

import rospy

from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from std_msgs.msg import String

from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2

import os
import requests

import PIL
from io import BytesIO
import base64


class wrapper(object):

    def __init__(self):
        self.data_pub = rospy.Publisher('int_topic', Int32, queue_size=1)
        self.img_pub = rospy.Publisher('image_topic', String, queue_size=1)

        # subscribe to ARI fisheye image data :
        # self.image_sub = rospy.Subscriber("/torso_back_camera/fisheye1/image_raw",Image,self.camera_callback)
        self.bridge = CvBridge()

    def camera_callback(self, data):
        # if subscribed to ARI image data we can modify and show image here :
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(
                data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)

        cv2.imshow('original_image', cv_image)

    def data_test(self):
        # sends two integers to server and returns the sum :
        request_dict = {"a": 4, "b": 3}
        url = "http://127.0.1.1:9099/api/matlab_run_cmd"
        response = requests.post(url, request_dict)

        rospy.loginfo(response.json())
        self.data_pub.publish(response.json())

    def image_send(self):
        # sends image data to server and returns it after modification :
        url = "http://127.0.1.1:9099/api/matlab_run_cmd"
        img = open(
            '/home/tika/catkin_ws/src/ros_server_communication/src/image.jpg', 'rb')
        conv_img = base64.b64encode(img.read())
        response = requests.post(url, data=conv_img)

        if response.ok:
            rospy.loginfo(response.content)
            # i = Image.open(BytesIO(response.content))
            self.img_pub.publish(response.content)
        else:
            rospy.loginfo("Something went wrong!")


def main():

    rospy.init_node('test_communication', anonymous=True)
    serv = wrapper()

    rospy.loginfo("ROS server communication layer is now started ...")

    # rate = rospy.Rate(1)
    # while not rospy.is_shutdown():
    #     serv.image_send()
    #     rate.sleep()

    serv.image_send()


if __name__ == '__main__':
    main()
