from setuptools import setup, find_packages

__author__ = 'Giulio Rossetti'
__license__ = "BSD 2 Clause"
__email__ = "giulio.rossetti@gmail.com"

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

setup(name='pquality',
      version='0.0.9',
      license='BSD-2-Clause',
      description='Community Discovery Partition Quality Indicators',
      url='https://github.com/GiulioRossetti/partition_quality',
      author='Giulio Rossetti',
      author_email='giulio.rossetti@gmail.com',
      use_2to3=True,
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 5 - Production/Stable',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: BSD License',

          "Operating System :: OS Independent",

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3'
      ],
      keywords=['complex-networks', 'community-discovery', 'quality-measures'],
      install_requires=['networkx', 'pandas', 'numpy', ''],
      packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test", "pquality.test", "pquality.test.*"]),
      )
