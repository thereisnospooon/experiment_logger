import os
import pathlib
import subprocess

from dataclasses import dataclass
import pickle
from experiment_logger.params import AbstractParams

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

    # Run actual experiment
    for iter in range(n_iterations):
        # ... Do some stuff
        loss = calc_loss()
        logger.watches.losses.append(loss)
        logger.watches.grads['dense_layer'] = current_grads
    logger.on_experiment_end()  # Save watches 

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
        self.watches = Watches()
        if git:
            self.save_git_snaptshot()
        # Last thing we do is to save the params.
        self.params.save_as_json()

    def save_git_snaptshot(self):
        """
        Save git branch and commit hash to params.
        Save diff to git patch file.
        """
        # Get the absolute path to your repository, 
        # no matter where you are running this code from.
        repo_path = self.params.src_path

        git_branch = subprocess.check_output(
            ["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode('UTF-8')

        git_commit_short_hash = subprocess.check_output(
            ["git", "-C", repo_path, "describe", "--always"]).strip().decode('UTF-8')

        git_diff = subprocess.check_output(
            ["git", "-C", repo_path, "diff"]).decode('UTF-8')  # notice no strip!

        self.params.git_branch = git_branch
        self.params.git_commit_short_hash = git_commit_short_hash

        if len(git_diff) > 0:
            git_diff_filepath = os.path.join(self.params.output_folder_path, 'git_diff.patch')
            with open(git_diff_filepath, 'w') as f:
                f.writelines(git_diff)

    def on_experiment_end(self):
        self.watches.save_as_pickle(self.params.output_folder_path)


@dataclass
class Watches:

    name:str = 'watches'

    def save_as_pickle(self, folder_name: str):
        """
        Save watched variables to pickle.

        Parameters
        ----------
        file_path : str
            path to folder to save watches to.
        """
        file_path = os.path.join(folder_name, self.name)
        with open(file_path, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_watches(path: str):
        with open(path, 'rb') as f:
            return pickle.load(f)