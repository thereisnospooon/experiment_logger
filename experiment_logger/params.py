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
        src_path: str = 'here'  # Required and also the typing is required
        output_folder_name_prefix: str = 'exp_2'  # Required and also the typing is required
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
        """
        Generate an instance of this 
        (or inherited) data class.

        Parameters
        ----------
        d : dict

        Returns
        -------
        An instance of a class that inherits from AbstractParams
        with all the fields as d.
        If d has keys that are not in the initial parameters of the class
        they will be added also. This means that if d contains the basic params required
        for the class it can then hold every other value also and it will be added to the new 
        instance.
        """
        init_params = cls.__dataclass_fields__.keys()
        init_fields = {}
        post_init_fields = {}
        for k, v in d.items():
            if k in init_params:
                init_fields[k] = v
            else:
                post_init_fields[k] = v
        new = cls(**init_fields)
        for k, v in post_init_fields.items():
            new.__setattr__(k, v)
        return new

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


@dataclass
class SampleParams(AbstractParams):
    src_path: str = 'bdddl'
    output_folder_name_prefix: str = 'nin'

if __name__ == "__main__":
    p = SampleParams()
    print(p.to_dict())