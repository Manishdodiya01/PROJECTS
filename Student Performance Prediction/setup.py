from setuptools import setup, find_packages
from typing import List



HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    THIS FUNCTION WILL RETURN THE LIST OF REQUIREMENTS
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name='mlproject',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    author='Manish Dodiya',
    author_email='dodiyamanish400@gmail.com',
    url='https://github.com/Manishdodiya01/Student_Performance_Prediction'

)
