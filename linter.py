#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by BUMshakalaka
# Copyright (c) 2017 BUMshakalaka
#
# License: MIT
#

"""This module exports the Nagelfar plugin class."""

from SublimeLinter.lint import Linter, util, persist
import os
import shlex
import string
import sublime


def get_project_folder():

    proj_file = sublime.active_window().project_file_name()
    if proj_file:
        return os.path.dirname(proj_file)

    # Use current file's folder when no project file is opened.
    proj_file = sublime.active_window().active_view().file_name()
    if proj_file:
        return os.path.dirname(proj_file)
    return '.'


def apply_template(s):
    """Substitute keys to proper values"""

    mapping = {
        'project_folder': get_project_folder(),
    }
    templ = string.Template(s)
    return templ.safe_substitute(mapping)


class Nagelfar(Linter):
    """Provides an interface to nagelfar."""

    syntax = 'tcl'

    # if "executable" is not found here, this linter won't be activated.
    # The cmd method created linter 'executable'
    if sublime.platform() == 'windows':
        # Windows OS would have "cmd"
        executable = 'cmd'
        cmd = 'cmd'
        version_args = None
        version_re = r'^.+\[Version\s(?P<version>\d+)\..+'
        version_requirement = '>=1'
    else:
        # A non-Windows OS
        executable = 'ls'
        cmd = 'ls'
        version_args = '--version'
        version_re = r'^.+>?\s(?P<version>\d+)\..+'
        version_requirement = '>=1'


    regex = r'^.*:?\s?Line\s+(?P<line>[0-9]+):\s(?:(?P<error>[E])|(?P<warning>[WN]))\s(?P<message>[^\"]+\"?(?P<near>[^\"]+).+\"?)'
    multiline = False
    line_col_base = (1, 0)
    tempfile_suffix = '-'
    default_settings = {
        'tcl_db': 'syntaxdb86.tcl',
        'additional_db': ['$project_folder\\.syntaxdb'],
    }

    def cmd(self):
        """
        Return the command line to be executed.
        We override this method, so we can change executable, add extra flags
        and include paths based on settings.
        """
        settings = self.get_view_settings()
        dbs = {}
        try:
            dbs['tcl_db'] = settings.get('tcl_db', self.default_settings['tcl_db'])
        except KeyError:
            if persist.settings.get('debug'):
                persist.printf('tcl_db not found in dict')
        try:
            dbs['additional_db'] = settings.get('additional_db', self.default_settings['additional_db'])
        except KeyError:
            if persist.settings.get('debug'):
                persist.printf('additional not found in dict')

        #Get linter folder. Only for windows
        #TODO: add other OS. If linter not exists, search PATH
        BASE_PATH = os.path.abspath(os.path.dirname(__file__))
        cmd = os.path.join(BASE_PATH, 'nagelfar_sh.exe')

        # depends of the user settings, add or not additional parameters to linter
        if len(dbs) > 0:
            cmd += ' -s '

        if 'tcl_db' in dbs:
            cmd += dbs['tcl_db'] + ' '

        cmd = cmd.replace('\\','\\\\')

        if 'additional_db' in dbs:
            cmd += apply_template(' '.join([shlex.quote(include) for include in dbs['additional_db']]))

        if persist.settings.get('debug'):
            persist.printf('cmd to execute: '+ cmd)
            persist.printf('Proj folder: '+ get_project_folder())
        return cmd