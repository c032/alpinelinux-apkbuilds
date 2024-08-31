import os
import subprocess
import sys


HERE = os.path.dirname(os.path.abspath(__file__))

SEARCH_DIRECTORIES = [
    os.path.join(HERE, 'main'),
    os.path.join(HERE, 'testing'),
]


def sh(cmd, args=None, working_directory=None):
    if not isinstance(cmd, str):
        raise TypeError('`cmd` must be str')
    if args is not None:
        if not isinstance(args, list):
            raise TypeError('`args` must be list')
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError('`args` must contain only values of type str')

    if working_directory is None:
        raise ValueError('`working_directory` is required')
    if not isinstance(working_directory, str):
        raise TypeError('`working_directory` must be str')
    if not os.path.isabs(working_directory):
        raise ValueError('`working_directory` must be an absolute path')

    subprocess.run(
        [cmd, *args],
        check=True,
        cwd=working_directory,
    )


def get_package_directories():
    for search_directory in SEARCH_DIRECTORIES:
        for root, dirs, files in os.walk(search_directory):
            dirs.sort()

            if 'APKBUILD' not in files:
                continue

            while len(dirs) > 0:
                dirs.pop()

            yield root


def main():
    for package_directory in get_package_directories():
        relpath = os.path.relpath(package_directory, start=HERE)
        print('===> {}'.format(relpath))
        sh('abuild', ['checksum'], working_directory=package_directory)
        sh('abuild', ['-k', '-r'], working_directory=package_directory)


if __name__ == '__main__':
    sys.exit(main())
