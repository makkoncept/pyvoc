from setuptools import setup


with open("README.md") as infile:
    long_description = infile.read()


setup(
    name="pyvoc",
    version="1.1.0",
    packages=["pyvoc"],
    description="cross-platform dictionary and vocabulary building command line tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://github.com/makkoncept/pyvoc",
    author="Mayank Nader",
    author_mail="nader.mayank@gmail.com",
    install_requires=["requests", "termcolor", "colorama"],
    entry_points={"console_scripts": ["pyvoc=pyvoc.pyvoc:main"]},
    include_package_data=True,
)
