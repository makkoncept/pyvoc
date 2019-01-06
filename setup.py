from setuptools import setup


setup(
    name="pyvoc",
    version="0.10",
    description="cross-platform dictionary and vocabulary building command line tool.",
    url="http://github.com/makkoncept/pyvoc",
    author="Mayank Nader",
    author_mail="nader.mayank@gmail.com",
    packages=["pyvoc"],
    install_requires=["requests", "termcolor", "colorama"],
    entry_points={"console_scripts": ["pyvoc=pyvoc.pyvoc:main"]},
)
