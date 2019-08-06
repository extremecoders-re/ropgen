from distutils.core import setup

setup(
    name = 'ropgen',
    packages = ['ropgen'],
    version = '1.0',
    license='MIT',
    description = 'A python module to facilitate in the generation of ROP chain exploit strings.',
    author = '0xec',
    author_email = 'extremecoders@hotmail.com',
    url = 'https://github.com/extremecoders-re/ropgen',
    download_url = 'https://github.com/extremecoders-re/ropgen/tarball/1.0',
    keywords = ['rop', 'rop-gadgets', 'rop-exploitation'],
    install_requires = ['texttable'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',        
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
    ],
)