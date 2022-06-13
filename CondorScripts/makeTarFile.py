import tarfile
import os, sys


exclude_files = [".tmp", ".log", ".stdout", ".stderr", ".git", "125","2016","2017", "2018",".0_2018", ".0_2017", ".0_2016", "plots", "Fiducial_XS",".0_2018_orig", "VM_add_to_info", ".0_2018",".0_1bin","allYear", "table", "slc7_amd64_gcc700"]

def filterFunction(tarinfo):
  """Helper function for the tarball creating.

  This function filters the unwanted files to add into the tarball creating.

  Arguments:
    tarinfo {type of tarinfo var} -- this is test

  Returns:
    returntype -- boolean function.
  """
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
