#from setuptools import setup, find_packages
import pkg_resources
# import find_packages,setuptools
from setuptools import find_packages, setup

setup(
    name='whitebearbake',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    entry_points={
                    'console_scripts':
                    [
                        'run-api=whitebearbake.run:run',
                        'run-cli=whitebearbake.run:cli',
                        'run-manage=whitebearbake.run:manage'

                    ],
                }
)
# from subprocess import check_output
# Override setuptools version normalization because it's stupid
# setuptools.extern.packaging.version.Version = pkg_resources.packaging.version.LegacyVersion # pylint: disable=E1101
# pkg_resources.packaging.version.Version = pkg_resources.packaging.version.LegacyVersion # pylint: disable=E1101

# def git_version(sha=False):
#     """ Extract version/iteration/sha from git tag """
#     try:
#         command = 'git describe --tags --long'
#         raw = check_output(command.split()).decode('utf-8').strip()
#     except:
#         return 'unknown'
#     version, build, commit = raw.split('-')[:3]
#     return '{}-{}{}'.format(version, build, '+'+commit if sha else '')

# __version__ = git_version()

# setuptools.setup(
#     name="whitebearbake",
#     version=__version__,
#     author="Deemarc-Burakitbumrung",
#     author_email="deemarc.br@gmail.com",
#     description=("My webapp to display dessert recipe"),
#     keywords="whitebearbake",
#     packages=setuptools.find_packages(),
#     include_package_data=True,
#     entry_points={
#                     'console_scripts':
#                     [
#                         'run-api=whitebearbake.run:run',
#                         'run-cli=whitebearbake.run:cli',
#                         'run-manage=whitebearbake.run:manage'

#                     ],
#                 }
# )
