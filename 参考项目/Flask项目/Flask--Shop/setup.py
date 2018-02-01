from setuptools import setup

setup(
    name='flask_shop',
    packages=['flask_shop'],
    include_package_data=True,
    install_requires=['flask',
                      'flask-sqlalchemy',
                      'flask-mail',
                      'flask-security',
                      'flask-babel',
                      'flask-uploads',
                      'pillow']
)
