import re
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile
import subprocess

def update_section(command: str, 
                   section: str, 
                   usage: bool = False) -> None:
    """
    Runs a command, captures its output, and replaces the contents of a section in the README.md file with the output.

    Parameters:
    command (str): The command to run as a string. The command should include any arguments.
    section (str): The name of the section in the README.md file to replace. This should be the text of the heading without the '## ' prefix.
    usage (bool): If True, the output will be dedented and wrapped in ```bash```. Default is False.

    Returns:
    None
    """
    # Run the command and capture the output
    result = subprocess.run(command.split(), capture_output=True, text=True)

    output = result.stdout + result.stderr
    if usage:
        output = output.lstrip('Usage: ')  # Remove 'Usage: ' from the beginning
        output = "\n".join([line.lstrip() for line in output.split('\n') if line.strip()])  # Dedent the lines and remove empty lines
        output = "\n```bash\n" + output + "\n```\n"  # Wrap the output in ```bash```
    else:
        output = "\n".join([line for line in output.split('\n') if line.strip()])  # Remove empty lines
        output = "\n" + output + "\n"
    print('------------------')
    print(output)
    print('------------------')

    readme = readfile("README.md")
    # Find the section and replace its contents with the output variable
    readme = re.sub(r'(## ' + section + r'\n)[\s\S]*?(?=(##|$))', r'\1' + output + '\n', readme)

    writefile("README.md", readme)

update_section('cloudmesh-installer', 'Usage', usage=True)
update_section('cloudmesh-installer help', 'Manual Page', usage=False)