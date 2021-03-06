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
    def __init__(self, executable, nagelfar_path):
        persist.printf('Builder initialized')
        self._executable = executable
        self._nagelfar = nagelfar_path
        self._scaner = pathScanner()

    def rebuild(self, masterPath):
        db_file = os.path.join(masterPath,'.syntaxdb')
        if os.path.exists(db_file) and os.path.getmtime(db_file) + 600.0 > time.time():
            if persist.settings.get('debug'):
                persist.printf('.syntaxdb exists and is was created within 10min ' + str(os.path.getmtime(db_file)) + ' os time ' + str(time.time()))
            return
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

        p = Popen([self._executable, join(self._nagelfar),'-header',db_file] + files, stdin=PIPE, stdout=PIPE, stderr=PIPE, startupinfo=si)
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

    #If tclsh is not available in the system - it makes no sense to go further
    executable = 'tclsh'
    cmd = 'tclsh'

    version_args = '\"' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version.tcl') + '\"'

    version_re = r'^Version:\s(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>=8.5'


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
        
        # take linter folder
        BASE_PATH = os.path.abspath(os.path.dirname(__file__))
        
        # take executable file from linter class (in this case tclsh)
        cmd = self.executable

        settings = self.get_view_settings()

        """
        Build syntax database basis using tcl, tm files form project folder, if file opened in project
        otherwise, do not create it.
        database is .syntaxdb file in project folder
        currently each time new database is build each time linter starts
        """
        bd = builder(cmd, os.path.join(BASE_PATH, 'nagelfar.kit'))
        bd.rebuild(get_project_folder())

        # Add negelfar.kit - the linter os-independent executable file which is executed by tclsh
        cmd += ' \"' + os.path.join(BASE_PATH, 'nagelfar.kit') + '\" '
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


        # depends of the user settings, add or not additional parameters to linter
        if len(dbs) > 0:
            cmd += ' -s '

        if 'tcl_db' in dbs:
            cmd += dbs['tcl_db'] + ' '

        #TODO: only on Windows??
        cmd = cmd.replace('\\','\\\\')

        if 'additional_db' in dbs:
            cmd += apply_template(' '.join([shlex.quote(include) for include in dbs['additional_db']]))

        if persist.settings.get('debug'):
            persist.printf('cmd to execute: '+ cmd)
        return cmd
