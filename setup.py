from setuptools import find_packages, setup


version = __import__('menuview').__version__


setup(
    name='django-menuview',
    version=version,
    url='https://github.com/eduardoklosowski/django-menuview',
    description='Make menu with View decorator',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    license='MIT',
    author='Eduardo Augusto Klosowski',
    author_email='eduardo_klosowski@yahoo.com',
    install_requires=[
        'Django',
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
