"""Setup file."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tidy_models',
    version='0.1.0',
    description='Boilerplate for keeping model results tidy.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    author='Brett D. Roads',
    author_email='brett.roads@gmail.com',
    license='Apache Licence 2.0',
    packages=['tidy_models'],
    python_requires='>=3.5, <3.9',
    install_requires=[
        'pandas'
    ],
    include_package_data=True,
    url='https://github.com/roads/tidy-models'
)
