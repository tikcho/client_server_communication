#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np


class Simple_Wrapper(object):

    def __init__(self):
    
        self.image_sub = rospy.Subscriber("/torso_back_camera/fisheye1/image_raw",Image,self.camera_callback)
        self.bridge_object = CvBridge()

    def camera_callback(self,data):
        # rospy.loginfo(data)
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
        
        # transform the image
        height, width, channels = cv_image.shape
        crop_img = cv_image[100:(height-100)][1:width]

        # show images
        cv2.imshow('original_image',cv_image)
        cv2.imshow('cropped_image',crop_img)

        # save images if pressed by s, or wait for ESC key to exit
        k=cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
        elif k == ord('s'):    
            cv2.imwrite('fisheye_image.jpeg', cv_image)
            cv2.destroyAllWindows()


def main():
    simple_wrapper_object = Simple_Wrapper()
    rospy.init_node('wrapper', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main()

