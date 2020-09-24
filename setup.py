from setuptools import setup

import pyvoc

with open("README.md") as infile:
    long_description = infile.read()


setup(
    name="pyvoc",
    version=pyvoc.__version__,
    packages=["pyvoc"],
    description="cross-platform dictionary and vocabulary building command line tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://github.com/makkoncept/pyvoc",
    author="Mayank Nader",
    author_email="nader.mayank@gmail.com",
    setup_requires=["wheel"],
    install_requires=["requests", "termcolor", "colorama", "pyenchant"],
    entry_points={"console_scripts": ["pyvoc=pyvoc.pyvoc:main"]},
    include_package_data=True,
)
