import tensorflow as tf
import numpy as np
import getopt
import sys
import json
import matplotlib.pyplot as plt
import os


class ModelNotFoundException(BaseException):
    pass


def get_saved_model():
    try:
        interpreter = tf.lite.Interpreter(model_path='model.tflite')
        classify_lite = interpreter.get_signature_runner('serving_default')
        return classify_lite
    except OSError as e:
        raise ModelNotFoundException(str(e))


def preprocess_image(image_path):
    # read an image file
    image = tf.io.read_file(image_path)
    # turn image into numerical tensors with RGB
    image = tf.image.decode_jpeg(image, channels=3)
    # resize image
    image = tf.image.resize(image, size=[400, 600])

    # uncomment for debugging
    # plt.figure(figsize=(10, 10))
    # plt.imshow(image)
    # plt.axis("off")
    #
    # plt.show()

    return image[None, :, :]  # Create a batch


HELP_STRING = "Usage: python tool.py --input_file /path/to/circuit.jpg"


def main(argv):
    input_file = 'examples/gen/0/circuit_0.jpg'

    try:
        opts, args = getopt.getopt(
            argv,
            "i",
            ["input_file="]
        )
    except getopt.GetoptError:
        print(HELP_STRING)
        sys.exit(2)

    # comment out this block to test
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print(HELP_STRING)
            sys.exit()
        elif opt in ["-i", "--input_file"]:
            input_file = arg

    if input_file is not None:
        print('\x1b[34m Opening the provided image... \n \x1b[37m')
        img = preprocess_image(input_file)
        print('\x1b[34m Loading the circuit identification model... \n \x1b[37m')
        model = get_saved_model()
        print('\x1b[34m Classifying the quantum circuit... \n \x1b[37m')
        predictions = model(rescaling_input=img)['dense_1']
        print('\x1b[34m Converting to QASM: \n \x1b[37m')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        class_map = json.loads('{ "0": 0, "1": 1, "2": 80, "3": 91, "4": 102, "5": 113, "6": 124, "7": 135, "8": 146, "9": 157, "10": 2, "11": 13, "12": 24, "13": 35, "14": 46, "15": 57, "16": 68, "17": 77, "18": 78, "19": 79, "20": 81, "21": 82, "22": 83, "23": 84, "24": 85, "25": 86, "26": 87, "27": 88, "28": 89, "29": 90, "30": 92, "31": 93, "32": 94, "33": 95, "34": 96, "35": 97, "36": 98, "37": 99, "38": 100, "39": 101, "40": 103, "41": 104, "42": 105, "43": 106, "44": 107, "45": 108, "46": 109, "47": 110, "48": 111, "49": 112, "50": 114, "51": 115, "52": 116, "53": 117, "54": 118, "55": 119, "56": 120, "57": 121, "58": 122, "59": 123, "60": 125, "61": 41, "62": 127, "63": 128, "64": 129, "65": 130, "66": 131, "67": 132, "68": 133, "69": 134, "70": 136, "71": 137, "72": 138, "73": 139, "74": 140, "75": 141, "76": 142, "77": 143, "78": 144, "79": 145, "80": 147, "81": 148, "82": 149, "83": 150, "84": 151, "85": 152, "86": 153, "87": 154, "88": 155, "89": 156, "90": 158, "91": 159, "92": 160, "93": 161, "94": 162, "95": 163, "96": 164, "97": 165, "98": 166, "99": 167, "100": 3, "101": 4, "102": 5, "103": 6, "104": 7, "105": 8, "106": 9, "107": 10, "108": 11, "109": 12, "110": 14, "111": 15, "112": 16, "113": 17, "114": 18, "115": 19, "116": 20, "117": 21, "118": 22, "119": 23, "120": 25, "121": 26, "122": 27, "123": 28, "124": 29, "125": 30, "126": 31, "127": 32, "128": 33, "129": 34, "130": 36, "131": 37, "132": 38, "133": 39, "134": 40, "135": 41, "136": 42, "137": 43, "138": 44, "139": 45, "140": 47, "141": 48, "142": 49, "143": 50, "144": 51, "145": 52, "146": 53, "147": 54, "148": 55, "149": 56, "150": 58, "151": 59, "152": 60, "153": 61, "154": 62, "155": 63, "156": 64, "157": 65, "158": 66, "159": 67, "160": 69, "161": 70, "162": 71, "163": 72, "164": 73, "165": 74, "166": 75, "167": 76}')
        qasm = open(f'{dir_path}/examples/gen/circuit_{list(class_map.keys())[list(class_map.values()).index(np.argmax(tf.nn.softmax(predictions)))]}.qasm')
        print(qasm.read() + "\n")
        print(f"confidence: {100 * np.max(tf.nn.softmax(predictions))} %")
        qasm.close()
    else:
        print("The input file is a required parameter.")


if __name__ == '__main__':
    main(sys.argv[1:])
