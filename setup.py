from setuptools import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="Byond_API",
    version='0.2.1',
    url="https://github.com/HaCsO/Byond-API",
    description="Simple way to take data from BYOND",
    packages=['Byond_API'],
    author_email="hacso@mail.ru",
    zip_file=False,
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)