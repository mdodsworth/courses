import os
from glob import glob
from zipfile import ZipFile

from cliff.app import App
from cliff.commandmanager import CommandManager
from kaggle_cli.config import Config
from kaggle_cli.download import Download
from kaggle_cli.submissions import Submissions
from kaggle_cli.submit import Submit


class KaggleCommandManager(CommandManager):

    def _load_commands(self):
        self.add_command('config', Config)
        self.add_command('download', Download)
        self.add_command('submit', Submit)
        self.add_command('submissions', Submissions)


class KaggleClient(App):

    def __init__(self):
        super(KaggleClient, self).__init__(
            description='API wrapper for the unofficial Kaggle command line tool.',
            version='0.1.0',
            command_manager=KaggleCommandManager('kaggle_cli')
        )

    def download_dataset(self, competition, target_path):
        current_path = os.getcwd()

        # pushd
        os.makedirs(target_path)
        os.chdir(target_path)

        try:
            self.run(['download', '-c', competition])

            # extract all downloaded zip files
            for zip_file_path in glob('*.zip'):
                with ZipFile(zip_file_path) as zip_file:
                    target_dir, _ = os.path.splitext(os.path.basename(zip_file_path))
                    zip_file.extractall()

                # clear away the zip files
                os.remove(zip_file_path)
        finally:
            # popd
            os.chdir(current_path)
