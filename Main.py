import argparse
import cv2

# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS={
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerKCF_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

# construct the argument parser and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', "--tracker", type=str, default='csrt',
                    help="OpenCV object tracker type")
parser.add_argument('-v', '--videoPath', type=str, default='165250-demo.mp4',
                    help="path to input video file")
args = vars(parser.parse_args())




def Main():
    # initial tracker
    (major, minor) = cv2.__version__.split(".")[:2]
    if int(major) == 3 and int(minor) < 3:
        tracker = cv2.Tracker_create(args["tracker"].upper())
    else:
        # tracker = OPENCV_OBJECT_TRACKERS[args.tracker]()
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()



    # if a video path was not supplied, grab the reference to the web cam
    if not args.get("videoPath", False):
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(1.0)
    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["videoPath"])



    # loop over frames from the video stream
    bbox = None
    while(vs.isOpened()):
        ret, frame  = vs.read()
        key = cv2.waitKey(1) & 0xFF

        # break condition
        if frame is None:
            break
        if key == ord('q'):
            break

        # set bbox
        if (bbox == None) or (key == ord('s')):
            bbox = cv2.selectROI("Frame",frame,fromCenter=False,showCrosshair=True)
            print("first box:",bbox)
            tracker.init(frame, bbox)

        # update bbox
        if bbox is not None:
            success, bbox = tracker.update(frame)
            x, y, w, h = bbox
            print("x,y,w,h:",x,y,w,h)
            cv2.rectangle(frame,(int(x), int(y)), (int(x+w), int(y+h)), (0,255,0), 2)
            
            cv2.putText(frame, "success" if success else "failure", (10,20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        
        # image show
        cv2.imshow("Frame",frame)
        cv2.waitKey(1)

    vs.release()
    cv2.destroyAllWindows()

 
if __name__ == "__main__":
    Main()
