from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='InsecamPy',
    version='0.0.3',
    packages=['InsecamPy'],
    url='https://github.com/OEUG99/InseCamCrawler',
    license='',
    author='OEUG99',
    author_email='iam@oweneugenio.com',
    description='Crawler for www.insecam.org',
    install_requires=requirements,
)