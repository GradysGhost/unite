from setuptools import setup

setup(name='unite',
      description      = 'Unite! - An extensible data aggregation API',
      author           = 'Ryan Jung',
      author_email     = 'gradysghost@gmail.com',
      version          = '0.0.1',
      url              = 'https://github.com/gradysghost/unite',
      license          = 'LICENSE',
      long_description = open('README.md').read(),
      install_requires = [
        'flask'
      ],
      packages         = [ 'unite' ]
)
