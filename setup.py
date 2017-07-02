from setuptools import setup


setup(
    name='localODquizz',
    py_modules=['localODquizz'],
    install_requires=[
        'Flask',
        'Flask-OAuth',
        'Flask-SQLAlchemy',
    ]
)
