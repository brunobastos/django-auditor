import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-auditor',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='This Django app logs changes of models objects in a simple and granular way.',
    long_description=README,
    url='https://github.com/brunobastos/django-auditor',
    author='Bruno Bastos',
    author_email='zerobruno@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Logging',
    ],
    keywords='django log audit',
)