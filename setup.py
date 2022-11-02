from setuptools import setup

setup(
    name="hooks",
    entry_points = {
        'console_scripts': [
            'check_msg = hooks.check_msg:main'
        ]
    }
)

