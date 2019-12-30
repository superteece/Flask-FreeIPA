"""
Flask-FreeIPA
-------------

This is the description for that library
"""
from setuptools import setup


setup(
    name='Flask-FreeIPA',
    version='1.0',
    url='https://github.com/superteece/Flask-FreeIPA.git',
    license='MIT',
    author='TC Johnson',
    author_email='TC@GeekMinistry.org',
    description='Extension to add FreeIPA\'s API to a Flask app',
    long_description=__doc__,
    packages=['flask_freeipa']
    #py_modules=['flask_freeipa'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'python_freeipa'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
