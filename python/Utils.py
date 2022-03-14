class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

def border_msg(msg):
    """Print message inside the border

    >>> border_msg('hello')
        +-----+
        |hello|
        +-----+

    Args:
        msg (str): message to print inside border
    """
    row = len(msg)+4
    h = ''.join(['+'] + ['-' *row] + ['+'])
    result= h + '\n'"|  "+msg+"  |"'\n' + h
    print(result)

def fixed_border_msg(msg):
    border = "="*51
    result = border + "\n" + msg + "\n" + border
    print(result)

def processCmd(cmd, lineNumber, quiet = 0):
    """This function is defined for processing of os command

    Args:
        cmd (str): The command to be run on the terminal
        lineNumber (int): The line number from where this function was invoked
        quiet (int, optional): Want to run the command in quite mode (Don't print anything) or print everything. Defaults to 0.

    Raises:
        RuntimeError: If the command failed then exit the program with exit code

    Returns:
        str: The full output of the command
    """
    output = '\n'
    print("="*51)
    print("[INFO]: Current working directory: {0}".format(os.getcwd()))
    print("[INFO]: {}#{} command:\n\t{}".format(os.path.basename(__file__), lineNumber, cmd))
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
    p.stdout.close()

    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))

    if (not quiet):
        print ('Output:\n   [{}] \n'.format(output))

    return output
