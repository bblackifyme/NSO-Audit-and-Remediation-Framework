from setuptools import setup, find_packages
from glob import glob
from os.path import basename, splitext


setup(
    name='audit_cli',
    version='0.01',
    author='Brandon Black',
    author_email='bblackifyme@gmail.com',
    description='CLI for executing the NSO Audit Framework',
    packages=['src'],
    include_package_data=True,
    install_requires=['click','requests', 'tabulate', 'csv', 'json'],
    entry_points='''
        [console_scripts]
        Audit_CLI=src.main:main
    ''',
)
