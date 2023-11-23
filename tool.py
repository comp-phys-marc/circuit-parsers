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
        # convert the model
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        # save the model
        with open('model.tflite', 'wb') as f:
            f.write(tflite_model)
        interpreter = tf.lite.Interpreter(model_path='model.tflite')
        classify_lite = interpreter.get_signature_runner('serving_default')
        return classify_lite
    except OSError as e:
        raise ModelNotFoundException(str(e))


def preprocess_image(image_path, image_size=180):
    img = tf.keras.utils.load_img(image_path, target_size=(image_size, image_size))
    img_array = tf.keras.utils.img_to_array(img)
    return tf.expand_dims(img_array, 0)  # Create a batch


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
        predictions = model(rescaling_input=img)['dense_1']
        print('\x1b[34m Converting to QASM: \n \x1b[37m')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        qasm = open(f'{dir_path}/examples/gen/circuit_{np.argmax(tf.nn.softmax(predictions))}.qasm')
        print(qasm.read() + "\n")
        print(f"confidence: {100 * np.max(tf.nn.softmax(predictions))} %")
        qasm.close()
    else:
        print("The input file is a required parameter.")


if __name__ == '__main__':
    main(sys.argv[1:])
