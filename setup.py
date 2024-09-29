from setuptools import setup,find_packages

setup(
   name='news_cluster',
   version='1.0',
   description='Clusteirng nepali news based on the incidents',
   packages=find_packages(),
   install_requires=['pandas','numpy','scikit-learn'],
   test = ['news_cluster.py'],
)
