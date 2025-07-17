import os
import subprocess  # For executing shell commands like git clone or python script.py

from crewai.tools import tool


@tool("Run Python Code From Repo")
def run_python_from_repo(repo_url: str, script_path: str, args: list = []) -> str:
    """
    Clones a Git repository and runs a specified Python script from it.
    repo_url: The URL of the Git repository.
    script_path: The path to the Python script within the repository.
    args: Optional arguments to pass to the Python script.
    """
    try:
        # Clone the repository (or update if already cloned)
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url],
            check=True,
            capture_output=True,
            text=True,
        )  #

        # Change directory into the cloned repo
        os.chdir(repo_name)  #

        # Execute the Python script
        command = ["python", script_path] + args  #
        result = subprocess.run(command, check=True, capture_output=True, text=True)  #
        return result.stdout
    except subprocess.CalledProcessError as e:  #
        return f"Error executing script: {e.stderr}"
    except Exception as e:  #
        return f"Error: {str(e)}"
    finally:
        # Clean up: Go back to the original directory (and optionally remove the cloned repo)
        # Be cautious with removing cloned repositories - only do this if appropriate.
        if "repo_name" in locals():
            os.chdir("..")
            subprocess.run(
                ["trash", "-rf", repo_name]
            )  # Uncomment to remove cloned repo
