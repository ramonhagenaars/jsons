import os
import re
import sys


def get_version():
    with open('setup.py', 'r') as f:
        setup_content = ' '.join(f.readlines())
        res = re.search("version='(.*?)'", setup_content)
        return res.group(1)


def get_exclusions():
    with open('.gitignore', 'r') as f:
        static_exclusions = [
            '.codecov.yml',
            '.coveragerc',
            '.travis.yml',
            '.git',
            '.gitignore',
            'build.py',
            'tox.ini',
            'jsons.egg-info',
            '_config.yml',
        ]
        lines = [f'--exclude="./{l.strip()}"'
                 for l in f.readlines() + static_exclusions
                 if l.strip()
                 and '*' not in l
                 and '#' not in l
                 and not l.startswith('/')]
        return ' '.join(lines)


filename = f'jsons-{get_version()}.tar.gz'

cmd_tar = (f'tar {get_exclusions()} '
           f'--exclude="{filename}" '
           f'-czf {filename} *')

cmd_wheel = 'python setup.py bdist_wheel'
cmd_mkdir_tar = 'mkdir tar'
cmd_move_tar = f'move {filename} tar'
cmd_deploy = 'twine upload dist/*'

arg_build = 'build'
arg_deploy = 'deploy'
args = [arg_build, arg_deploy]

if __name__ == '__main__':
    if os.name == 'nt':
        if len(sys.argv) < 2:
            print(f'Expecting one of the following commands: {", ".join(args)}')
        elif sys.argv[1] == arg_build:
            os.system(cmd_wheel)
            os.system(cmd_tar)
            os.system(cmd_mkdir_tar)
            os.system(cmd_move_tar)
        elif sys.argv[1] == arg_deploy:
            os.system(cmd_deploy)
        else:
            print(f'Unsupported command "{sys.argv[1]}"')
    else:
        print('This script is intended for use on Windows only')
