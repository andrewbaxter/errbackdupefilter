import os
from setuptools import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name='scrapy-errbackdupefilter',
    version='0.0.1',
    description='Filtered duplicate requests trigger the errback',
    long_description=LONG_DESC,
    author='Andrew Baxter',
    author_email='afb2@wustl.edu',
    url='https://github.com/andrewbaxter/errbackdupefilter',
    license='BSD',
    py_modules=['errbackdupefilter'],
    install_requires=[
        'Scrapy>=0.14',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
)
