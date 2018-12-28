from setuptools import setup


setup(
    name='pyvoc',
    version='0.10',
    description='dictionary cum vocabulary manager',
    author='Mayank Nader',
    author_mail='nader.mayank@gmail.com',
    packages=['pyvoc'],
    install_requires=['requests'],
    entry_points={"console_scripts": ["pyvoc=pyvoc.pyvoc:main"]},
)
