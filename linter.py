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
from os import walk, system
from os.path import join, splitext, abspath
from subprocess import Popen, PIPE, STARTUPINFO, STARTF_USESHOWWINDOW
from re import search

def convertPath(path):
    """ Convert /D/path/path2 -> D:/path/path2"""
    if sublime.platform() == 'windows':
        path = path.split('/')
        path[1] = path[1] + ':'
        path = "\\".join(path[1:])
    return path

def get_project_folder():
    proj_file = sublime.active_window().project_file_name()
    if proj_file:
        project_data = sublime.active_window().project_data()   
        if project_data['folders'][0]['path'] is '.':
            return os.path.dirname(proj_file)
        return convertPath(project_data['folders'][0]['path'])

    #File without project - return None
    #Because of rebuild function. If we return file folder, it can happen that rebuild would like to scane whole disc
    return 


def apply_template(s):
    """Substitute keys to proper values"""

    mapping = {
        'project_folder': get_project_folder(),
    }
    templ = string.Template(s)
    return templ.safe_substitute(mapping)

class builder():
    def __init__(self, nagelfar_path):
        persist.printf('Builder initialized')
        self._nagelfar = nagelfar_path
        self._scaner = pathScanner()

    def rebuild(self, masterPath):
        persist.printf('Rebuilding in folder {}'.format(masterPath))
        if masterPath is None:
            persist.printf('Nothing to rebuild')
            return

        self._scaner.scan(masterPath, ['.tcl', '.tm'])
        si = STARTUPINFO()
        si.dwFlags |= STARTF_USESHOWWINDOW
        files = []
        for file in self._scaner:
            if search('.*syntaxbuild.tcl', file) or search('.*syntaxdb.tcl', file):
                continue
            #persist.printf('Rebuilding for file {}'.format(file))
            files.append(file)

        p = Popen([join(self._nagelfar).replace('\\','\\\\'),'-header',join(masterPath,'.syntaxdb')] + files, stdin=PIPE, stdout=PIPE, stderr=PIPE, startupinfo=si)
        output, err = p.communicate()

        if persist.settings.get('debug'):
            persist.printf('output: ' + str(output) + ', error: ' + str(err))

class pathScanner():
    '''Initialize, scand and create iterator'''

    def __init__(self):
        self._files = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._files) == 0:
            raise StopIteration
        else:
            return self._files.pop()

    def scan(self, path, extensions):
        '''Append to _files'''
        self._files = []
        for (dirpath, dirnames, filenames) in walk(path):
            for file in filenames:
                if splitext(file)[1] in extensions:
                    self._files.append(abspath(join(dirpath, file)))
        return 0

class Nagelfar(Linter):
    """Provides an interface to nagelfar."""

    syntax = 'tcl'

    #TODO: add other OS. Currently only windows supported

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
        
        #TODO: If linter not exists, search PATH
        #Get linter folder which is used to get nagelfar_sh.exe file
        BASE_PATH = os.path.abspath(os.path.dirname(__file__))
        settings = self.get_view_settings()

        """
        Build syntax database basis using tcl, tm files form project folder, if file opened in project
        otherwise, do not create it.
        database is .syntaxdb file in project folder
        currently each time new database is build each time linter starts
        """
        bd = builder(os.path.join(BASE_PATH, 'nagelfar_sh.exe'))
        bd.rebuild(get_project_folder())

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
        return cmd
