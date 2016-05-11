#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.getcwd(), './'))

import shutil
import rescpy
import glob


src_dir = '/mnt/dir_x'
dest_resource_dir = os.path.join(os.getcwd(), 'relative_dir')
    
         
def get_symbols(x):
    sdir_sym = os.path.join(src_dir, 'symbols')

    for sym in ('ace', 'jack', 'king', 'queen'):
        x.create_symonoff(sym, sdir_sym)

    #for sym in ('tony_stark', 'pepper_pots', 'black_widow'):
    #    x.create_symblock(sym, sdir_sym)
    # a_b is a directory
    # c is file name
    x.create_symblock('a_b', sdir_sym, 'c')
    

def get_resources_background():
    ddir_background = os.path.join(dest_resource_dir, 'background')
    if not os.path.exists(ddir_background):
        os.makedirs(ddir_background)
    shutil.copy(os.path.join(src_dir, "background/background.png"), os.path.join(ddir_background, 'background.png'))        
    shutil.copy(os.path.join(src_dir, "background/feature_background.png"), os.path.join(ddir_background, 'feature_background.png'))        
    
 
    
if __name__ == "__main__":
    """Read resources."""
    dest = 'symbol_python'
    x = rescpy.ResCpy(dest_resource_dir, dest)
    
    #get_resources_background()
    get_symbols(x)
    
