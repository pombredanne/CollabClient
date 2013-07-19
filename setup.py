from setuptools import setup, find_packages

setup(
    name='ccollab_client',
    version='0.1.0',
    author='Shawn Crosby',
    author_email='scrosby@salesforce.com',
    packages=find_packages(),
    license='Be Real',
    description='Wrapper for code collab command line',
    long_description=open('README.txt').read(),
)