import tensorflow as tf
import PIL
import getopt
import sys


class ModelNotFoundException(BaseException):
    pass


def get_saved_model():
    try:
        model = tf.saved_model.load(f'saved_models/trained_model')
        return model
    except OSError as e:
        raise ModelNotFoundException(str(e))


HELP_STRING = "Usage: python tool.py -i /path/to/circuit.jpg"


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
    # for opt, arg in opts:
    #     if opt in ["-h", "--help"]:
    #         print(HELP_STRING)
    #         sys.exit()
    #     elif opt in ["-i", "--input_files"]:
    #         input_file = arg

    if input_file is not None:
        print('\x1b[34m Opening the provided image... \n \x1b[37m')
        img = PIL.Image.open(input_file)
        print('\x1b[34m Loading the circuit identification model... \n \x1b[37m')
        model = get_saved_model()
        print('\x1b[34m Classifying the quantum circuit... \n \x1b[37m')
        predictions = model(img)
    else:
        print("The input file is a required parameter.")


if __name__ == '__main__':
    main(sys.argv[1:])
