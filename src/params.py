from datetime import datetime
from dataclasses import dataclass
import os
import json

from optparse import OptionParser

@dataclass
class AbstractParams:
    """
    Abstract parameters class.
    If we want to run an experiment with some params,
    we just inherit this class and add our params to it.
    
    2 required parameters - 
    src_path: str - parent folder where all experiment are saved.
    output_folder_name_prefix: str - prefix of subfolder where experiment data should be saved.

    Usage - 
    from experiment_logger import Params

    @dataclass  # IMPORTANT!
    class ExperimentParams(AbstractParams):
        src_path = 'here'  # Required
        output_folder_name_prefix = 'exp_2'  # Required
        lr: float = 0.3
        n_layers: int = 100
        activation: str = 'relu'

    >> p = ExperimentParams()
    >> print(p.n_layers)
    >> 100
    >> p.__dict__
    {'lr': 0.3
    'n_layers': 10
    'activation': 'relu',
    'src_path': 'here',
    ...}

    ---------------------------------
    In the above example, saving the params to p.output_folder_path
    will be - <src_path>/<output_folder_name_prefix + time of start>/
    """
    src_path: str 
    output_folder_name_prefix: str 
    start_time_str : str = None
    output_folder_name: str = None
    output_folder_path: str = None
    params_name = 'params'

    def __post_init__(self):
        self.start_time_str = datetime.today().strftime('%d_%m_%Y__%H_%M_%S')
        self.output_folder_name = f'{self.output_folder_name_prefix}_{self.start_time_str}'
        self.output_folder_path = os.path.join(self.src_path, self.output_folder_name)

    def to_dict(self):
        return self.__dict__

    def save_as_json(self, file_path: str = None):
        """
        Save parameters to json.

        Parameters
        ----------
        file_path : str, optional
            If None, default behaviour is to save to "<self.output_folder_path>/self.params_name + '.json'"
        """
        d = self.to_dict()
        sorted_dict = {k: d[k] for k in sorted(d.keys())}
        if not file_path:
            file_path = os.path.join(self.output_folder_path, self.params_name + '.json')
        json.dump(sorted_dict, open(file_path, 'w'), indent=4)

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)

    @classmethod
    def from_json(cls, file_path: str):
        d = json.load(open(file_path, 'r'))
        return cls.from_dict(d)

    @classmethod
    def from_parser(cls, parser: OptionParser):
        """
        Create a new instance of this class
        from a commnad-line args parser.
        Can be used in inheritance.

        Parameters
        ----------
        parser : OptionParser
            Command-line args parser.

        Returns
        -------
        An instance of the class (if the class inherits from Params then it will return
        and instance of the child class).
        """
        input_params, _ = parser.parse_args()
        kwargs = {key: value for key, value in input_params.__dict__.items() if value is not None}
        params = cls(**kwargs)
        return params