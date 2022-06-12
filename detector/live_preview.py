import traceback
import cv2
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def _render_results(results):
    try:
        results.render()
        return results.imgs[0]
    except:
        print(traceback.print_exc())

def generate_live_detector_preview(camera):
    while True:
        frame = camera.read()
        result = model(frame)
        rendered_image = _render_results(result)
        ret, frame = cv2.imencode('.jpg', rendered_image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')