import tensorflow as tf
import numpy as np
import getopt
import sys
import os


class ModelNotFoundException(BaseException):
    pass


def get_saved_model():
    try:
        # get file dir
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # load model
        model = tf.saved_model.load(f'{dir_path}/saved_models/trained_model')
        return model
    except OSError as e:
        raise ModelNotFoundException(str(e))


def preprocess_image(image_path, image_size=180):
    # read an image file
    image = tf.io.read_file(image_path)
    # turn image into numerical tensors with RGBs
    image = tf.image.decode_jpeg(image, channels=3)
    # convert color values from 0-255 to 0-1 #Normaliizations
    image = tf.image.convert_image_dtype(image, tf.float32)
    # resize image
    image = tf.image.resize(image, size=[image_size, image_size])

    return image[None, :, :]


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
        elif opt in ["-i", "--input_files"]:
            input_file = arg

    if input_file is not None:
        print('\x1b[34m Opening the provided image... \n \x1b[37m')
        img = preprocess_image(input_file)
        print('\x1b[34m Loading the circuit identification model... \n \x1b[37m')
        model = get_saved_model()
        print('\x1b[34m Classifying the quantum circuit... \n \x1b[37m')
        predictions = model(img)
        print('\x1b[34m Converting to QASM: \n \x1b[37m')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        qasm = open(f'{dir_path}/examples/gen/circuit_{list(np.array(predictions)[0]).index(min(np.array(predictions)[0]))}.qasm')
        print(qasm.read())
        qasm.close()
    else:
        print("The input file is a required parameter.")


if __name__ == '__main__':
    main(sys.argv[1:])
