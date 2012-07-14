#! /usr/bin/env pysh
#-*-python-*-

"""This module runs the refactoring code on a sequence of reference files in order
to test automatic rmap refactoring.   Based on the reference file and a given
context,  this code determines which rmap to modify and attempts to add the new
reference file to it.
"""

import sys
import random
import shutil
import os.path

from crds import (rmap, log, refactor, pysh, matches, utils)
import crds.client as client

def newfile(fname):
   root, ext = os.path.splitext(fname)
   return "./" + os.path.basename(root) + "_new" + ext

def new_references(new_file):
    for line in open(new_file):
        if not line.strip():
            continue
        new_reference = line.split()[0]
        yield new_reference

def main(context, new_references):
    for reference in new_references:
        
        pmap = rmap.get_cached_mapping(context)

        try:
           refpath = pmap.locate.locate_server_reference(reference)
        except KeyError:
           log.error("Can't locate reference file", repr(reference))
           continue

        try:
            instrument, filekind, old_rmap_path = get_corresponding_rmap(context, refpath)
        except Exception, exc:
            log.error("Failed getting corresponding rmap for", repr(reference), repr(str(exc)))
            continue

        log.info("Reference", os.path.basename(old_rmap_path), os.path.basename(refpath))

        new_rmap_path = "./temp.rmap"
            
        new_refpath = newfile(refpath)      # a different looking file to insert
        pysh.sh("ln -s ${refpath} ${new_refpath}")
        
        mtchs = [x[1:] for x in matches.find_full_match_paths(context, os.path.basename(reference))]
        if mtchs:
            keys = simplified_path(mtchs[0])[0]
            values = [simplified_path(match)[1] for match in mtchs]
            log.info("Original matches at:", keys, values) 
        
        try:
            pysh.sh("rm -f ${new_rmap_path}")
            actions = refactor.rmap_insert_references(
               old_rmap_path, new_rmap_path, [new_refpath])
            log.write("diffing", repr(new_rmap_path), "from", repr(old_rmap_path))
            sys.stdout.flush()
            sys.stderr.flush()
            pysh.sh("diff -c ${old_rmap_path} ${new_rmap_path}")
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception, exc:
            log.error("Exception", str(exc))
        
        pysh.sh("rm -f ${new_rmap_path} ${new_refpath}")

    sys.stdout.flush()
    sys.stderr.flush()
    log.write()
    log.standard_status()
    
def simplified_path(match_path):
    keys = []
    values = []
    for tup in match_path:
        for key,val in tup:
            keys.append(key)
            values.append(val)
    return keys, tuple(values)
    
def get_corresponding_rmap(context, refpath):
    """Return the path to the rmap which *would* refer to `reference` in `context.`
    """
    pmap = rmap.get_cached_mapping(context)
    instrument, filekind = utils.get_file_properties(pmap.observatory, refpath)
    old_rmap = rmap.locate_mapping(pmap.get_imap(instrument).get_rmap(filekind).name)
    return instrument, filekind, old_rmap

if __name__ == "__main__":
    log.set_verbose(60)
    context = sys.argv[1]
    if sys.argv[2].startswith("@"):
        references = new_references(sys.argv[2][1:])
    else:
        references = sys.argv[2:]
    main(context, references)
