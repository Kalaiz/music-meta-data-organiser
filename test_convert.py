import os 
import logging
import shutil
import sys
import pytest
from convert import convert_to_specific_format
import util_test


BASE_PATH = "test"
TEST_DATA_DIRECTORY = "test-data"
TEST_RUN_DIRECTORY = "test-run-data"
CONVERT_DIRECTORY = "convert"

class TestConvertToSpecificFormat:

    @pytest.fixture(autouse=True)
    def caplog(self, caplog):
        self.caplog = caplog

    @classmethod
    def setup_class(cls):
        current_path =  os.getcwd() 
        absolute_test_run_path = os.path.join(current_path,BASE_PATH,TEST_RUN_DIRECTORY)
        absolute_test_data_path = os.path.join(current_path,BASE_PATH,TEST_DATA_DIRECTORY)
        logging.debug("Setting up: convert to specific format test")
        if os.path.exists(absolute_test_run_path):
            logging.debug("Previous test run was shut off abruptly; Removing old test run folder.")
            cls.remove_test_run_folder(absolute_test_run_path)
        shutil.copytree(src=absolute_test_data_path,dst=absolute_test_run_path)
        cls.absolute_test_run_directory = absolute_test_run_path
        logging.basicConfig(stream=sys.stdout)

    @classmethod
    def teardown_class(cls):
        logging.debug("Tearing down: convert to sepcific format test")
        cls.remove_test_run_folder(cls.absolute_test_run_directory)

    @classmethod
    def remove_test_run_folder(cls,absolute_test_run_path):
        shutil.rmtree(absolute_test_run_path)

    def test_if_audio_file_to_mp3(self):
        convert_directory_path = os.path.join(self.__class__.absolute_test_run_directory,CONVERT_DIRECTORY)

        file_paths = util_test.get_file_paths(convert_directory_path,has_basic)
        
        for file_path in file_paths:
            try:
                convert_to_specific_format(file_path,format="mp3")
            except Exception as e: 
                logging.error("Exception "+ str(e))
                assert False

        file_names = util_test.get_file_names(convert_directory_path,has_basic)
        are_files_mp3 = list(map(lambda file_name: file_name.split('.')[-1]=="mp3",file_names))
        assert all(are_files_mp3)


    def test_invalid_path(self):
        try:
            convert_to_specific_format("/invalid///")
        except:
             assert False
        captured_console_content = self.caplog.text
        assert "error" in captured_console_content.lower()


    def test_if_old_file_exist(self):
        convert_directory_path = os.path.join(self.__class__.absolute_test_run_directory,CONVERT_DIRECTORY)

        file_paths = util_test.get_file_paths(convert_directory_path,has_old_file_exist)

        for file_path in file_paths:
            try:
                convert_to_specific_format(file_path,format="mp3")
            except Exception as e: 
                logging.error("Exception "+ str(e))
                assert False
        
        new_file_paths = util_test.get_file_paths(convert_directory_path,has_old_file_exist)

        for old_file_path in file_paths:
            if old_file_path in new_file_paths:
                assert False
        
        assert True

def has_old_file_exist(file_name):
    return "old-file" in file_name.lower()

def has_basic(file_name):
    return "basic" in file_name.lower()





