import os
from setuptools import setup, find_packages


version = '1.0.0.dev0'


extras_require = {
    'tests': [
        'pytest',
    ],
}


setup(name='opengever.apiclient',
      version=version,
      description='API Client for OneGov GEVER',

      long_description=open('README.rst').read() + '\n'
      + open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      keywords='onegov gever opengever api client',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/opengever.apiclient',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['opengever', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'setuptools',
      ],

      extras_require=extras_require)
