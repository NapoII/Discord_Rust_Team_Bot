import subprocess
import os

def get_last_commit_comment(folder_path="."):
    """
    Retrieve the last Git commit comment for a specified folder.

    Parameters:
    - folder_path (str): The relative path to the target folder. Default is the current directory.

    Returns:
    - str: The last Git commit comment.
    """
    try:
        # Get the absolute path of the parent directory
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        target_directory = os.path.join(current_directory, folder_path)

        # Git command to retrieve the last commit comment
        git_command = "git log -1 --pretty=%B"

        # Execute the Git command in the target directory and decode the output
        commit_comment = subprocess.check_output(git_command, cwd=target_directory, shell=True, text=True)

        return commit_comment.strip()

    except subprocess.CalledProcessError:
        return "Error retrieving the commit comment."


last_commit_comment = get_last_commit_comment()

# Print the last Git commit comment
print("Last Git commit comment:", last_commit_comment)
