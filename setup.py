from distutils.core import setup
setup(
    name='stockscrape',         # How you named your package folder (MyLib)
    packages=['stockscrape'],   # Chose the same as "name"
    version='2.0',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Stockscrape scrapes data from Yahoo Finance and retrieves it in a JSON format.',
    author='rawsashimi1604, Gavin Loo',                   # Type in your name
    author_email='looweiren@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/rawsashimi1604/stockscrap_v2',
    # I explain this later on
    download_url='https://github.com/rawsashimi1604/stockscrap_v2/archive/refs/tags/v2.0.tar.gz',
    # Keywords that define your package best
    keywords=['FINANCE', 'WEBSCRAPING', 'STOCKS'],
    install_requires=[            # I get to this in a second
        'beautifulsoup4',
        'certifi',
        'charset-normalizer',
        'click',
        'colorama',
        'idna',
        'itsdangerous',
        'MarkupSafe',
        'numpy',
        'pandas',
        'python-dateutil',
        'pytz',
        'requests',
        'six',
        'soupsieve',
        'urllib3'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
