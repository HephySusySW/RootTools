'''Sample constructed from a list of files'''

# Standard imports
import ROOT
import os, subprocess

# Logging
import logging

# Base class
from  RootTools.Sample.SampleBase import SampleBase, EmptySampleError

# Helpers
import RootTools.tools.helpers as helpers

def readNormalization(filename):
    with open(filename, 'r') as fin:
        for line in fin:
            if any( [x in line for x in ['All Events', 'Sum Weights'] ] ):
                sumW = float(line.split()[2])
                return sumW

class SampleFromFiles( SampleBase ):

    def __init__(self, name, files, treeName = 'Events', maxN = None):

        super(SampleFromFiles, self).__init__(name=name, treeName = treeName)

        self.__logger = logging.getLogger("Logger."+__name__)

        self.maxN = maxN if not (maxN and maxN<0) else None 

        # Adding and checking files
        for filename in files: 
            if not helpers.checkRootFile(filename, checkForObjects=[treeName] ):
                self.__logger.warning( "Could not read file %s",  filename )
            else:
                self.files.append(filename)

        # Don't allow empty samples
        if len(self.files) == 0: 
            raise EmptySampleError("No valid file found for sample {0}.".format(self.name) )

        self.__logger.info("Loaded SampleFromFiles %s. Total number of files : %i. Bad files: %i.", self.name, len(files), len(files)-len(self.files) ) 
