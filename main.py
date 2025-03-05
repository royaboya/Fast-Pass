from controller import Controller
from encrypt_model import EncryptModel
from command_line_view import CommandLineView

import argparse

if __name__ == "__main__":
    
    encrypt_model = EncryptModel()
    command_line_view = CommandLineView()
    controller = Controller(model=encrypt_model, view=command_line_view)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clear", action="store_true", help="clears logs")
    
    args = parser.parse_args()
    
    if args.clear:
        controller.clear_logs()
    else:
        controller.run()
