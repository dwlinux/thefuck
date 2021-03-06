import re
from thefuck import shells


patterns = (
    r"mv: cannot move '[^']*' to '([^']*)': No such file or directory",
    r"mv: cannot move '[^']*' to '([^']*)': Not a directory",
    r"cp: cannot create regular file '([^']*)': No such file or directory",
    r"cp: cannot create regular file '([^']*)': Not a directory",
)


def match(command, settings):
    for pattern in patterns:
        if re.search(pattern, command.stderr):
            return True

    return False


def get_new_command(command, settings):
    for pattern in patterns:
        file = re.findall(pattern, command.stderr)

        if file:
            file = file[0]
            dir = file[0:file.rfind('/')]

            formatme = shells.and_('mkdir -p {}', '{}')
            return formatme.format(dir, command.script)
