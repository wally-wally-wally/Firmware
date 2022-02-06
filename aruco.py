import numpy as np
import cv2
import sys

ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
}

TYPE_DEF = 'DICT_5X5_100'
ARUCO_DIR_DEF = 'img/'
SIZE_DEF = 200
MARKER_LENGTH_DEF = 0.02

# Generate an ArUco image
# output = path to output folder to save ArUCo tag
# id = ID of ArUCo tag to generate
# type = type of ArUCo tag to generate
# size = Size of the ArUCo tag in pixels
# visualize = display the ArUco marker

# return: True on success, false on failure
def genAruco(id, output = ARUCO_DIR_DEF, type = TYPE_DEF, size = SIZE_DEF, visualize = False):
    # Check to see if the dictionary is supported
    if ARUCO_DICT.get(type, None) is None:
	    #print(f"ArUCo tag type 'type' is not supported")
        return False

    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[type])

    print("Generating ArUCo tag of type '{}' with ID '{}'".format(type, id))
    tag = np.zeros((size, size, 1), dtype="uint8")
    cv2.aruco.drawMarker(arucoDict, id, size, tag, 1)

    # Save the tag generated
    tag_name = f'{output}/{type}_id_{id}.png'
    cv2.imwrite(tag_name, tag)

    if visualize is True:
        cv2.imshow("ArUCo Tag", tag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return True


# Inverts the rvec and tvec
# Changes the perspective from the arUco to Wally to the perspective
# of Wally to the arUco
# Meant for internal use only
def invert(rvec, tvec):
    rvec, tvec = rvec.reshape((3, 1)), tvec.reshape((3, 1))
    R, _ = cv2.Rodrigues(rvec)
    R = np.matrix(R).T
    invTvec = np.dot(R, np.matrix(-tvec))
    invRvec, _ = cv2.Rodrigues(R)
    return invRvec, invTvec


# imgPath - Path to image
# kMatrixPath - Path to calibration matrix (numpy file)
# distCoeffPath - Path to distortion coefficients (numpy file)
# markerLength - Length of the marker (metres)
# visualize - display the ArUco marker(s) with the pose

# return: False on failure; Otherwise returns rotation and translation vectors
def estimatePose(imgPath, type = TYPE_DEF, kMatrixPath = 'camera_calibration/calibration_matrix.npy',
                    distCoeffPath = 'camera_calibration/distortion_coefficients.npy', markerLength = MARKER_LENGTH_DEF, visualize = False):

    if ARUCO_DICT.get(type, None) is None:
        print(f"ArUCo tag type 'type' is not supported")
        return False

    image = cv2.imread(imgPath)
    h,w,_ = image.shape
    width = 600
    height = int(width*(h/w))
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[type])
    parameters = cv2.aruco.DetectorParameters_create()

    matrix_coefficients = np.load(kMatrixPath)
    distortion_coefficients = np.load(distCoeffPath)

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)

    # If markers are detected
    rvec = []
    tvec = []
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            r, t = cv2.aruco.estimatePoseSingleMarkers(corners[i], markerLength, matrix_coefficients,
                                                                       distortion_coefficients)
            invR, invT = invert(r, t)
            rvec.append(invR)
            tvec.append(invT)

            if (visualize is True):
                # Draw a square around the markers
                cv2.aruco.drawDetectedMarkers(image, corners)
                # Draw Axis
                cv2.aruco.drawAxis(image, matrix_coefficients, distortion_coefficients, r, t, 0.01)
                cv2.imshow('Estimated Pose', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    return rvec, tvec
