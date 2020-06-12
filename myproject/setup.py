from setuptools import setup
def readme():
    with open('README.md') as f:
        return f.read()

setup(name='myproject',
      version='0.0.1',
      description='Demo pacman game',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      ],
      url='https://github.com/tainp98/pacman',
      author='tainp98',
      author_email='nguyenphutaibk@gmail.com',
      keywords='core package',
      license='MIT',
      packages=['myproject'],
      install_requires=['numpy','pygame'],
      include_package_data=True,
      zip_safe=False)