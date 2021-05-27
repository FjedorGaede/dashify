from setuptools import setup, find_packages
import pathlib
import os

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='dashify',
    version='0.1.0',
    author='Robin Schulte, Fjedor Gaede',
    author_email='r.schulte@lvm.de, fjedor.gaede@gmail.com',
    description="Easy integration of Dash into Flask app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://bitbucket.lvm.de/bitbucket/scm/~m13729/dwh_generators.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
                    'Flask',
                    'Dash',
                    'Dash-Auth==1.4.1'
                    ],

)