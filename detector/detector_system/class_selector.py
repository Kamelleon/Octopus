import logging

logging.basicConfig(filename='detector_logger.txt',
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


class ClassSelector:
    CLASS_NAMES = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                   'traffic light',
                   'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                   'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
                   'frisbee',
                   'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                   'surfboard',
                   'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                   'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                   'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                   'cell phone',
                   'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                   'teddy bear',
                   'hair drier', 'toothbrush']

    @staticmethod
    def choose(selected_class_names_list=None, select_all_classes=False):
        names = []
        if not select_all_classes or selected_class_names_list is not None:
            for list_object in selected_class_names_list:
                index_of_object = ClassSelector.CLASS_NAMES.index(list_object)
                names.append(index_of_object)
        else:
            for list_object in ClassSelector.CLASS_NAMES:
                index_of_object = ClassSelector.CLASS_NAMES.index(list_object)
                names.append(index_of_object)
        return names