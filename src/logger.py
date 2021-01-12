from datetime import datetime
from dataclasses import dataclass
import os
import json

from optparse import OptionParser


class Logger:
    """
    This class supports the following behaviours - 
    * Init the experiment directory inside a given parent directory.
    * Dictionary of configurations parameters.
    * Save parameters to json file.
    * Optional - Create a tag/branch in git with the experiment code snapshot.

    For example - 

    from experiment_logger import Logger

    logger = Logger(parent_folder='<folder>',
                    code_snapshots=False, experiment_name='network_try_2',
                    config={'n_layers':3, 'n_iterations':100, 'convergence_thresh':1e-6})
    logger.config_update('lr', 0.01)
    """
    def __init__(self):
        pass

@dataclass
class Params:
    """
    Holds the parameters of the experiment.
    @dataclass means that we can assign parameters as if they are class attributes.
    For example - 

    from experiment_logger impoer Params

    >> p = Params()
    >> p.lr = 0.1
    >> p.n_layers = 10
    >> p.activation = 'relu'
    >> print(p.n_layers)
    >> 10
    >> p.__dict__
    {'lr': 0.1
    'n_layers': 10
    'activation': 'relu'}
    """
    src_path: str = '.'
    output_folder_name_prefix: str = 'output'
    start_time_str : str = None
    output_folder_name: str = None
    output_folder_path: str = None

    def __init__(self, output_folder_name):
        self.output_folder_name_prefix = output_folder_name
    def __post_init__(self):
        self.start_time_str = datetime.today().strftime('%d_%m_%Y__%H_%M_%S')
        self.output_folder_name = f'{self.output_folder_name_prefix}_{self.start_time_str}'
        self.output_folder_path = os.path.join(self.src_path, self.output_folder_name)

    def to_dict(self):
        return self.__dict__

    def to_json(self, file_path: str = None):
        d = self.to_dict()
        sorted_dict = {k: d[k] for k in sorted(d.keys())}
        json.dump(sorted_dict, open(file_path, 'w'), indent=4)

    @staticmethod
    def from_dict(d: dict):
        return Params(**d)

    @staticmethod
    def from_json(file_path: str):
        d = json.load(open(file_path, 'r'))
        return Params.from_dict(d)

    @staticmethod
    def from_parser(parser: OptionParser):
        input_params, _ = parser.parse_args()
        kwargs = {key: value for key, value in input_params.__dict__.items() if value is not None}
        params = Params(**kwargs)
        return params