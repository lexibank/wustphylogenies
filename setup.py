from setuptools import setup


setup(
    name='lexibank_bodtstnew',
    py_modules=['lexibank_bodtstnew'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'bodtstnew=lexibank_bodtstnew:Dataset',
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
