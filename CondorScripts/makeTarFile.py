import tarfile
import os, sys


  
exclude_files = [".tmp", ".log", ".stdout", ".stderr", "log_2017", "log_2018", "log_2016", "2016_backup_mass4l_160", "2017_backup_mass4l_160", "2018_backup_mass4l_160", "2016", "2017", "2018", "xs_125.0_1bin", "xs_125.0_2018_125p0", "xs_125.0_2017_125p0", "xs_125.0_2016_125p0", "xs_125.0_5bins", "xs_125.0_6bins", "xs_125.0_7bins", "xs_125.0_8bins", "xs_125.0_9bins","plots_125p0", "plots", "table", "table_125p0", "templatesXS_2016", "templatesXS_2017", "templatesXS_2018"] 


def filterFunction(tarinfo):
  """Helper function for the tarball creating.

  This function filters the unwanted files to add into the tarball creating.

  Arguments:
    tarinfo {type of tarinfo var} -- this is test

  Returns:
    returntype -- boolean function.
  """

  # print "exclude self.files: ",self.exclude_files
  # if os.path.splitext(tarinfo.name)[1] in exclude_files:
  if ((os.path.splitext(tarinfo.name)[1] in exclude_files) or (os.path.splitext(tarinfo.name)[0].split('/')[-1] in exclude_files)):
    return None
  else:
    return tarinfo

def make_tarfile(source_dir, output_filename):
  """Function to create the tarball.

  This function creates the tarball of a given directory.

  Arguments:
    output_filename {string} -- Output file name of the tarball.
    source_dir {string} -- Name of directory for which you need to make the tarball.
  """
  with tarfile.open(output_filename, "w:gz") as tar:
    print 'make_tarfile:: Started creating tar file...'
    tar.add(source_dir, arcname=os.path.basename(source_dir), filter=filterFunction)
    print 'make_tarfile:: Done...'
