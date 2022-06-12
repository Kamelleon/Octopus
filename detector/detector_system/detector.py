import logging
import traceback
import datetime
from PIL import Image
import yaml
from yaml.loader import SafeLoader
import os
import time
import torch
import cv2
from pathlib import Path
from class_selector import ClassSelector
logging.basicConfig(filename='detector_logger.txt',
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


class YoloDetectionModel:
    def __init__(self, classes_for_detection, model_type="yolov5l", telegram_bot=None, config_file=None):

        if torch.cuda.is_available():
            self.device_used_for_detections = "cuda:0"
        else:
            self.device_used_for_detections = "cpu"

        self.config_file = config_file
        self.yolo_repository = 'ultralytics/yolov5'
        self.yolo_model_type = model_type
        self._classes_for_detection = classes_for_detection
        self.yolo_classes = ClassSelector.choose(self._classes_for_detection)
        self.minimum_probability_for_detection = float(config_file["detector"]["confidence"])
        self.minimum_number_of_objects_to_consider_as_detection = 1
        self.model = None
        self.skip_outdated_pictures = bool(config_file["detector"]["skip_outdated_frames"])

        if self.skip_outdated_pictures:
            print("Skipping outdated pictures: Enabled")
        else:
            print("Skipping outdated pictures: Disabled")

        self.image_manager = ImageManager()
        if telegram_bot is not None:
            self.telegram_bot = telegram_bot
        else:
            self.telegram_bot = None



        self.load()

    def load(self):
        print(f"""
        [i] Trying to load pretrained YOLO model with selected settings:
        -------------------------------------------------
        Device used for detections: {self.device_used_for_detections}
        YOLO repository: {self.yolo_repository}
        YOLO model type: {self.yolo_model_type}
        YOLO repository location: GitHub (remote download)
        Selected classes: {self._classes_for_detection}
        Minimum probability for detection: {self.minimum_probability_for_detection}
        -------------------------------------------------
        """)

        print("[~] Loading model...")
        logging.info("Loading model...")
        self.model = torch.hub.load(self.yolo_repository, self.yolo_model_type, pretrained=True, source="github")
        self.images_blacklist = []
        self.model.classes = self.yolo_classes
        self.model.conf = self.minimum_probability_for_detection
        print("[+] Model has been loaded")
        logging.info("Model has been loaded")

    def perform_detection_on_images_from_current_folder(self):
        print("[~] Starting detection (it may take a while...)")
        logging.info("Starting detection...")
        while True:
            try:
                detection_start_time = time.time()
                for file in os.listdir(os.getcwd()):
                    file_is_image = file.endswith(".jpg") or file.endswith(".png")
                    if file_is_image:
                        image = file
                        image_name_without_extension = Path(image).stem

                        if self.skip_outdated_pictures:
                            last_time_of_modification_in_seconds = self.image_manager.get_modification_timedelta(image)
                            if last_time_of_modification_in_seconds > 10:

                                if not image_name_without_extension in self.images_blacklist:
                                    self.telegram_bot.add_message_to_queue(image_name_without_extension,
                                                                           f"Kamera {image_name_without_extension} nie odpowiada. ({time.strftime('%H:%M:%S')})")
                                    self.images_blacklist.append(image_name_without_extension)
                                    continue
                                else:
                                    continue
                            else:
                                if image_name_without_extension in self.images_blacklist:
                                    self.telegram_bot.add_message_to_queue(image_name_without_extension,
                                                                           f"Kamera {image_name_without_extension} znów działa. ({time.strftime('%H:%M:%S')})")
                                    self.images_blacklist.remove(image_name_without_extension)

                        image = cv2.imread(image)

                        if "areas" in self.config_file["cameras"][f"{image_name_without_extension}"]:
                            self.perform_detection_on_areas(image, image_name_without_extension)
                        else:
                            self.perform_detection_without_areas(image, image_name_without_extension)

                print(f"[i] Detection performed in:", time.time() - detection_start_time, "seconds")
                logging.info("Detection successfully performed")

            except KeyboardInterrupt:
                print("Keyboard interrupt detected. Exiting...")
                os._exit(1)

    def perform_detection_without_areas(self, image, image_name_without_extension):
        results = self.model(image)
        model_has_detected_something = len(
            results.pandas().xyxy[0]) >= self.minimum_number_of_objects_to_consider_as_detection

        if model_has_detected_something:
            print(f"[!] Detected something on: {image_name_without_extension}")
            logging.info(f"Detected something on: {image_name_without_extension}")

            rendered_image = self._render_results(results)
            self.image_manager.create_new_folder_with_image_name(image_name_without_extension)
            self.image_manager.save_rendered_image_to_folder(rendered_image, using_areas=False)
            logging.info(f"Wysyłam zdjęcie: {image_name_without_extension}")
            if self.telegram_bot is not None:
                self.telegram_bot.add_message_with_image_to_queue(
                    self.image_manager.current_image_path,
                    f"Wykryto człowieka na kamerze {image_name_without_extension} "
                    f"o godzinie {time.strftime('%H:%M:%S')}.")

    def perform_detection_on_areas(self, image, image_name_without_extension):
        image_with_areas = image.copy()
        self.draw_areas_on_image(image_with_areas, image_name_without_extension)
        for item in self.config_file['cameras'][image_name_without_extension]['areas']:
            rectangle_points = item.split(",")

            x1 = int(rectangle_points[0])
            y1 = int(rectangle_points[1])
            x2 = int(rectangle_points[2])
            y2 = int(rectangle_points[3])

            if x1 < x2 and y1 < y2:
                cropped_area = image[y1:y2, x1:x2]
            elif x1 > x2 and y1 > y2:
                cropped_area = image[y2:y1, x2:x1]
            elif x1 > x2 and y1 < y2:
                cropped_area = image[y1:y2, x2:x1]
            elif x1 < x2 and y1 > y2:
                cropped_area = image[y2:y1, x1:x2]

            try:
                cropped_area = cv2.cvtColor(cropped_area, cv2.COLOR_BGR2RGB)
                results = self.model(cropped_area)  # Perform detection
            except:
                logging.error("Error occurred during performing detection")
                logging.error(f"{traceback.format_exc()}")
                continue

            model_has_detected_something = len(
                results.pandas().xyxy[
                    0]) >= self.minimum_number_of_objects_to_consider_as_detection

            if model_has_detected_something:
                print(f"[!] Detected something on: {image_name_without_extension}")
                logging.info(f"Detected something on: {image_name_without_extension}")
                rendered_image = self._render_results(results)
                if x1 < x2 and y1 < y2:
                    image_with_areas[y1:y2, x1:x2] = rendered_image
                elif x1 > x2 and y1 > y2:
                    image_with_areas[y2:y1, x2:x1] = rendered_image
                elif x1 > x2 and y1 < y2:
                    image_with_areas[y1:y2, x2:x1] = rendered_image
                elif x1 < x2 and y1 > y2:
                    image_with_areas[y2:y1, x1:x2] = rendered_image

                self.image_manager.create_new_folder_with_image_name(
                    image_name_without_extension)
                self.image_manager.save_rendered_image_to_folder(image_with_areas,
                                                                 using_areas=True)

                logging.info(f"Wysyłam zdjęcie: {image_name_without_extension}")
                if self.telegram_bot is not None:
                        self.telegram_bot.add_message_with_image_to_queue(
                            self.image_manager.current_image_path,
                            f"Wykryto człowieka na kamerze {image_name_without_extension} "
                            f"o godzinie {time.strftime('%H:%M:%S')}.")

    def draw_areas_on_image(self, image, image_name_without_extension):
        for item in self.config_file['cameras'][image_name_without_extension]['areas']:
            rectangle_points = item.split(",")

            x1 = int(rectangle_points[0])
            y1 = int(rectangle_points[1])
            x2 = int(rectangle_points[2])
            y2 = int(rectangle_points[3])

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)

    def _render_results(self, results):
        try:
            results.render()
            for img in results.imgs:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                rendered_image = Image.fromarray(img)
            return rendered_image
        except:
            logging.error("Could not render results")
            logging.error(f"{traceback.format_exc()}")


class ImageManager:
    def __init__(self):
        self.current_folder_name = ""
        self.current_image_path = ""

    def get_modification_timedelta(self, file):
        modification_time = os.path.getmtime(file)
        epoch_time = int(time.time())
        tdelta = int(epoch_time - modification_time)
        return tdelta

    def create_new_folder_with_image_name(self, image_name_without_extension):
        try:
            current_date = DateTimePicker.get_current_date()
            if not os.path.isdir(f"{current_date}"):
                os.mkdir(f"{current_date}")
            if not os.path.isdir(f"{current_date}/{image_name_without_extension}"):
                os.mkdir(f"{current_date}/{image_name_without_extension}")
            self.current_folder_name = image_name_without_extension
        except:
            logging.error("Could not create a folder with image name")
            logging.error(f"{traceback.format_exc()}")
            os._exit(1)

    def save_rendered_image_to_folder(self, rendered_image, using_areas=False):
        try:
            current_date = DateTimePicker.get_current_date()
            current_time = DateTimePicker.get_current_time()
            if using_areas:
                cv2.imwrite(f"{current_date}/{self.current_folder_name}/{current_time}.jpg", rendered_image)
            else:
                rendered_image.save(f"{current_date}/{self.current_folder_name}/{current_time}.jpg", format="JPEG")
            self.current_image_path = f"{current_date}/{self.current_folder_name}/{current_time}.jpg"
        except:
            logging.error("Could not save an image to a folder")
            logging.error(f"{traceback.format_exc()}")
            os._exit(1)

class DateTimePicker:
    @staticmethod
    def get_current_date():
        return datetime.date.today().strftime("%d-%m-%Y")

    @staticmethod
    def get_current_time():
        return time.strftime('%H_%M_%S')

def run():
    pass