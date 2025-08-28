"""
{{ cookiecutter.project_name }} info file
"""

from importlib.metadata import version

__application__ = "{{ cookiecutter.friendly_name }}"
__version__ = version(__application__)
