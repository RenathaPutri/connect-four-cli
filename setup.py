from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='connect-four-cli',
    version='1',
    packages=['connect-four-cli'],
    url='https://github.com/RenathaPutri/connect-four-cli',
    license='MIT',
    author='Renatha Putri',
    author_email='queennatha444@gmail.com',
    description='This package contains implementation of a command-line Connect Four game with Google Gemini AI integrated into it.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={
        "console_scripts": [
            "connect-four-cli=connect-four-cli.cfour:main",
        ]
    }
)