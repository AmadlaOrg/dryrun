import unittest
from unittest.mock import patch

from click.testing import CliRunner
from dryrun.dryrun import setup, cli
import tempfile
import os


class TestDryRun(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()  # Clean up the temporary directory after the test

    @patch('os.path.expanduser')
    def test_setup(self, mock_expanduser):
        mock_expanduser.return_value = self.temp_dir.name  # Return the path to the temporary directory

        test_dirs = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures'))

        result = self.runner.invoke(cli,
                                    ['setup',
                                     '--name',
                                     'test',
                                     '--path',
                                     test_dirs,
                                     '--time',
                                     '1',
                                     '--reboot',
                                     '--strict'])

        # Check that the command didn't fail and completed successfully
        self.assertEqual(result.exit_code, 0)

        # You can add other assertions here, like checking if the files were correctly created,
        # if the config file has the correct content, etc.
        # For example, check if the completion message is printed
        self.assertIn("Setup completed for dryrun 'test'.", result.output)

        # Additional tests to ensure the correct directory structure has been created
        dryrun_dir = os.path.join(self.temp_dir.name, '.dryrun', 'test')
        #print(dryrun_dir)
        self.assertTrue(os.path.exists(dryrun_dir))  # Check that the .dryrun directory has been created
        self.tearDown()  # Clean up the temporary directory after the test

    @patch('os.path.expanduser')
    def test_old_and_new_dirs_created(self, mock_expanduser):
        mock_expanduser.return_value = self.temp_dir.name
        test_dirs = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures'))
        self.runner.invoke(cli,
                           ['setup', '--name', 'test', '--path', test_dirs, '--time', '1', '--reboot', '--strict'])
        dryrun_dir = os.path.join(self.temp_dir.name, '.dryrun', 'test')
        self.assertTrue(os.path.exists(os.path.join(dryrun_dir, 'old')))
        self.assertTrue(os.path.exists(os.path.join(dryrun_dir, 'new')))
        self.tearDown()

    @patch('os.path.expanduser')
    def test_config_toml_created(self, mock_expanduser):
        mock_expanduser.return_value = self.temp_dir.name
        test_dirs = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures'))
        self.runner.invoke(cli, ['setup', '--name', 'test', '--path', test_dirs, '--time', '1', '--reboot', '--strict'])
        dryrun_dir = os.path.join(self.temp_dir.name, '.dryrun', 'test')
        config_toml = os.path.join(dryrun_dir, 'config.toml')
        self.assertTrue(os.path.exists(config_toml))
        with open(config_toml, 'r') as f:
            content = f.read()
        self.assertIn('name = "test"', content)
        self.assertIn(f'paths = [\'{test_dirs}\']', content)
        self.assertIn('time = "1"', content)
        self.assertIn('reboot = true', content)
        self.assertIn('strict = true', content)
        self.tearDown()

    @patch('os.path.expanduser')
    def test_invalid_name_raises_error(self, mock_expanduser):
        mock_expanduser.return_value = self.temp_dir.name
        test_dirs = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures'))
        result = self.runner.invoke(cli,
                                    ['setup', '--name', 'invalid/name', '--path', test_dirs, '--time', '1', '--reboot',
                                     '--strict'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('Name should only contain alphanumeric characters, underscores, and hyphens.', result.output)
        self.tearDown()

    @patch('os.path.expanduser')
    def test_multiple_paths(self, mock_expanduser):
        mock_expanduser.return_value = self.temp_dir.name
        test_dirs = [
            str(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'fixtures', 'multiple_paths', 'dir1', 'etc', 'subject')),
            str(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'fixtures', 'multiple_paths', 'dir2', 'etc', 'subject'))]

        #print(test_dirs)

        result = self.runner.invoke(cli, ['setup', '--name', 'test', '--path', test_dirs[0], '--path', test_dirs[1],
                                          '--time', '1', '--reboot', '--strict'])

        # Print the result output to see the actual error
        #print(result.output)

        self.assertEqual(result.exit_code, 0)
        dryrun_dir = os.path.join(self.temp_dir.name, '.dryrun', 'test')
        #print(dryrun_dir)
        config_toml = os.path.join(dryrun_dir, 'config.toml')
        self.assertTrue(os.path.exists(config_toml))
        with open(config_toml, 'r') as f:
            content = f.read()
        self.assertIn(f'paths = [\'{test_dirs[0]}\', \'{test_dirs[1]}\']', content)
        print(os.path.abspath(os.path.join(dryrun_dir, 'old', 'dir1')))
        print(os.path.exists(os.path.join(dryrun_dir, 'old', 'dir1')))
        self.assertTrue(os.path.exists(os.path.join(dryrun_dir, 'old', 'dir1')))
        #self.assertTrue(os.path.exists(os.path.join(dryrun_dir, 'old', 'dir2')))
        self.tearDown()


if __name__ == '__main__':
    unittest.main()
