from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:

    requirements_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()

                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)

    except FileNotFoundError:
        print('file not found error requirement.txt')

    return requirements_list

print(get_requirements())

setup(
    name='Network Security',
    version='0.0.1',
    author='Youssef Hessain',
    author_email='youssefhussainnasr2000@gmail.com',
    description='Network Security prediction app',
    packages=find_packages(),
    requires=get_requirements(),
)