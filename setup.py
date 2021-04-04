from setuptools import setup, find_packages

install_requires = ['arcade>=2.5.6']

with open("README.md", "r") as longfile:
    long_description = longfile.read()

setup(
    name='CatBurglar',
    version='0.0.1',
    install_requires=install_requires,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
           'catburglar=CatBurglar.main:main'
        ]
    },
    python_requires='>=3.7'
)