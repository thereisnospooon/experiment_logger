import os
from dataclasses import dataclass
import json
from src.params import AbstractParams

class Logger:
    """
    This class supports the following behaviours - 
    * Init the experiment directory inside a given parent directory.
    * Dictionary of configurations parameters.
    * Save parameters to json file.
    * Optional - Create a tag/branch in git with the experiment code snapshot.

    For example - 

    from experiment_logger import Logger
    from params import AbstractParams

    @dataclass
    class MyParams(AbstractParams):
        my_attribute = 30

    p = MyParams()
    logger = Logger(p)
    
    # Init watches
    logger.watches.losses = []
    logger.watches.grads = {}
    for iter in range(n_iterations):
        # ... Do some stuff
        loss = calc_loss()
        logger.watches.losses.append(loss)
        logger.watches.grads['blublu'] = current_grads

    """
    def __init__(self, params: AbstractParams, git=True):
        """
        Logger class to keep track of experiments.

        Parameters
        ----------
        params : AbstractParams
            a class that inherits from AbstractParams of
            parameters of this experiment.
        git : bool, optional
            If True, save current code snapshot (hash of last commit, branch name, and git diff).
            Assumes that params.src_path is a git repo.
        """
        self.params = params
        os.mkdir(self.params.output_folder_path)
        self.params.save_as_json()
        self.watches = Watches()

    def on_experiment_end(self):
        self.watches.save_as_json(self.params.output_folder_path)


@dataclass
class Watches:

    name:str = 'watches'

    def save_as_json(self, folder_name: str):
        """
        Save watched variables to json.

        Parameters
        ----------
        file_path : str
            path to folder to save watches to.
        """
        d = self.__dict__
        sorted_dict = {k: d[k] for k in sorted(d.keys())}
        file_path = os.path.join(folder_name, self.name + '.json')
        json.dump(sorted_dict, open(file_path, 'w'), indent=4)