import re

from setuptools import setup


def get_version(filename):
    '''
    Return package version as listed in `__version__` in `filename`.
    '''
    with open(filename, 'r') as fp:
        init_py = fp.read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('pytest_flake8dir.py')


with open('README.rst', 'r') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', 'r') as history_file:
    history = history_file.read().replace('.. :changelog:', '')


setup(
    name='pytest-flake8dir',
    version=version,
    description='A pytest fixture for testing flake8 plugins.',
    long_description=readme + '\n\n' + history,
    author='Adam Johnson',
    author_email='me@adamj.eu',
    url='https://github.com/adamchainz/pytest-flake8dir',
    py_modules=['pytest_flake8dir'],
    include_package_data=True,
    install_requires=[
        'flake8',
        'pytest',
    ],
    python_requires='>=3.4',
    license='ISC License',
    zip_safe=False,
    keywords='pytest, flake8',
    entry_points={
        'pytest11': ['flake8dir = pytest_flake8dir'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
