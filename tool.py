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
        # while its a 1-1 mapping it isn’t exactly in-order numerically, rather its alphanumerically.
        sorted_ints = map(lambda j: int(j), sorted([str(i) for i in range(6000)]))
        class_map = {}
        for k, nt in enumerate(sorted_ints):
            class_map[str(k)] = nt
        qasm = open(f'{dir_path}/examples/gen/circuit_{list(class_map.keys())[list(class_map.values()).index(np.argmax(tf.nn.softmax(predictions)))]}.qasm')
        print(qasm.read() + "\n")
        print(f"confidence: {100 * np.max(tf.nn.softmax(predictions))} %")
        qasm.close()
    else:
        print("The input file is a required parameter.")


if __name__ == '__main__':
    main(sys.argv[1:])
