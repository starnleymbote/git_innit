
from databricks.sdk.runtime import *
import os, importlib.util, concurrent.futures


dbfs_directory = '../dist'
try:
    dbfs_directory = dbutils.widgets.get('dbfs_directory')
except:
    pass

if importlib.util.find_spec('utils') is None: # Package is not installed
    os.system(f'pip install --force-reinstall {dbfs_directory}/dqwrapper-1.0.0-py3-none-any.whl')

if importlib.util.find_spec('timestream_utils') is None: # Package is not installed
    os.system(f'pip install --force-reinstall {dbfs_directory}/timestream_utils-0.0.8-py3-none-any.whl')

from utils.helper_functions import HelperFunctions
from utils.error_handler import ErrorHandling
from utils.exceptions import Severity
from utils.context import Context
from datetime import datetime

class GenerateText(Context):
    """
    To be deleted: spike for testing comming files in git using code.
    """

    def generate_text_file(self, text):
        """
        Create a file autonomasly and print hello in it
        """
        with open('test.txt', 'a') as f:
            # Write 'Hello' to the file
            f.write(f'Hello this is the current time {text}\n')
        
    def commit_and_push(self, message):
        """
        This method is responsible for commiting and pushing the generated SQLs
        """

        branch = "dev"
        #Git pull any changes so far
        git_pull = f"git pull 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:@github.com origin {branch}"

        print(f"Git commint command {git_pull}")

        os.system(git_pull)

        git_add = f"git add ."

        print(f"The git add command {git_add}")
        
        os.system(git_add)

        git_commit = f"git commit -m {message}"

        print(f"Git commit command {git_commit}")

        os.system(git_commit)

        git_push = f"git push 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:@github.com origin {branch}"

        print(f"Git push command {git_push}")
        
        os.system(git_push)

        # print("Done!!!")
        
    # def commit_and_push(self, message):
    #     """
    #     This method is responsible for commiting and pushing the generated SQLs
    #     """

    #     branch = "dev"
    #     #Git pull any changes so far
    #     git_pull = f"git pull "


    #     os.system(git_pull)

    #     git_add = f"git add ."

 
        
    #     os.system(git_add)

    #     git_commit = f"git commit -m {message}"



    #     os.system(git_commit)

    #     git_push = f"git push"

        
    #     os.system(git_push)

    #     print("Done!!!")

    def main(self):

        print("About to write to our file")
        text = datetime.now()
        self.generate_text_file(text)
        print("File has been created ")

        message = "\'Commit the generated texts\'"
        print("Starting to commit the changes")
        self.commit_and_push(message)
        print("Done pushing the changes")
        
    def __call__(self):
        """
        The call method that executes the DBTGenerateModelsSQLFiles task.
        """
        try:        
            if int(Context.skip_task) != 1:                 
                #run this task
                self.main()
                
            else:
                print("Task Skipped")

        except Exception as e:
            ErrorHandling(
                job_id=Context.dbt_run_id,
                process='DBTGenerateModelsSQLFiles',
                exception={
                    'message': '''An error occurred while running dbx DBTGenerateModelsSQLFiles task.''',
                    'details': f'{str(e)}',
                    'severity': Severity.ERROR
                }
            )()

if __name__ == '__main__':
    #run cleanup job
    GenerateText()()