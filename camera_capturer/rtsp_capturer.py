import threading
import time
from threading import Thread

import cv2
import rtsp

import threading

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


from imutils.video import VideoStream


class Capturer:
    restricted = []
    generators = []
    def __init__(self, rtsp_ip, port, suffix):
        self.rtsp_ip = rtsp_ip
        self.vs = VideoStream(src=f'rtsp://{rtsp_ip}:{port}{suffix}').start()
        self.outputFrame = None
        self.lock = threading.Lock()
        self.t = StoppableThread(target=self.detect_motion)
        self.t.daemon = True
        self.t.start()

    def detect_motion(self):
        while True:
            try:
                time.sleep(0.1)
                frame = self.vs.read()

                with self.lock:
                    self.outputFrame = frame.copy()
            except:
                break
        i = 0
        for camera_object in Capturer.generators:
            if self.rtsp_ip in camera_object.keys():
                Capturer.generators.pop(i)
                Capturer.restricted.pop(i)
            i += 1
        self.vs.stop()

    def generate(self):
        while True:
            time.sleep(0.1)
            with self.lock:
                if self.outputFrame is None:
                    continue

                flag, encodedImage = cv2.imencode(".jpg", self.outputFrame)

                if not flag:
                    continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + encodedImage.tobytes() + b'\r\n\r\n')
