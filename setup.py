from distutils.core import setup

setup(
  name = 'eodclient',
  packages = ['eodclient'],
  version = '1.0.1.dev1',
  description = 'A python client for interacting with the EOD Historical Data api',
  author = 'surfer190',
  author_email = 'shutch190@gmail.com',
  url = 'https://github.com/surfer190/EOD-Historical-Data-client',
  download_url = 'https://github.com/surfer190/EOD-Historical-Data-client/archive/1.0.1.dev1.tar.gz',
  keywords = ['api', 'client', 'eod', 'eod historical data'],
  classifiers = [],
  license='GPLv3',
  install_requires=['requests>=2,<3'],
  python_requires='>=3.6',
)