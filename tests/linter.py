"""
This module uses pylint to check the code format
"""

import pylint.lint
pylint_opts = ['../main.py', '../notification.py']
pylint.lint.Run(pylint_opts)
