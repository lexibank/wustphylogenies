from setuptools import setup


setup(
    name='lexibank_bodtphylogeny',
    py_modules=['lexibank_bodtphylogeny'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'bodtphylogeny=lexibank_bodtphylogeny:Dataset',
        ],
        'cldfbench.commands':[
            'bodtphylogeny = bodtphylogenycommands',
        ]
    },
    install_requires=[
        'cldfbench',
        'pylexibank',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
