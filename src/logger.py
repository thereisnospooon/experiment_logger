import os
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
    p = Params()
    logger = Logger(p)
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
        """
        self.params = params
        os.mkdir(self.params.output_folder_path)
        pass

