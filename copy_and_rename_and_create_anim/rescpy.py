import os
import shutil
import glob

class ResCpy:
    
    
    def __init__(self, res_dir, dest):
        self.__res_dir__ = res_dir
        self.sym_dir_ = dest

    #Create dunngen.ini and copy .png files from src_dir 
    #to os.path.join(self.__res_dir__, dst_rdir) if num is 1 or 
    #to os.path.join(self.__res_dir__, dst_rdir, n) where n = 1, 2, ..., num if num > 1.
    def create_sprite(self, src_dir, dst_rdir, num = 1, direction = 'forward'):
        if num == 1:
            rdir = dst_rdir
        else:
            rdir = os.path.join(dst_rdir, '1')
        dst = os.path.join(self.__res_dir__, rdir)
        if not os.path.exists(dst):
            os.makedirs(dst)

        #copy .png files and create dunngen.ini
        png_files = [filename for filename in os.listdir(src_dir) if filename.endswith('.png')]
        for filename in png_files:
            shutil.copy(os.path.join(src_dir, filename), dst)
        with open(os.path.join(dst, 'dunngen.ini'), 'w') as f:
            f.write("[images]\nforce_sprites=YES\n\n[sprite]\nftime=20 fps\ndirection={0}".format(direction))

        #create .png.link files and create dunngen.ini for n = 2 to num
        for i in range(2, num+1):
            dst = os.path.join(self.__res_dir__, dst_rdir, str(i))
            if not os.path.exists(dst):
                os.makedirs(dst)
            for filename in png_files:
                with open(os.path.join(dst, filename+'.link'), 'w') as f:
                    f.write('"/' + rdir + '/' + filename + '"')
            with open(os.path.join(dst, 'dunngen.ini'), 'w') as f:
                f.write("[images]\nforce_sprites=YES\n\n[sprite]\nftime=20 fps\ndirection={0}".format(direction))

    def create_symnonwin(self, sym, src_dir):
        dst = os.path.join(self.__res_dir__, self.sym_dir_, sym, 'nonwin')
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copy(os.path.join(src_dir, sym+'.png'), dst)
        with open(os.path.join(dst, 'dunngen.ini'), 'w') as f:
            f.write("[images]\nforce_sprites=YES\n\n[sprite]\nftime=2 fps\natime=3000000")

    def create_symwin(self, sym, src_dir, src_dir_win):
        self.create_symnonwin(sym, src_dir)
        
        dst = os.path.join(self.__res_dir__, self.sym_dir_, sym, 'win')
        if not os.path.exists(dst):
            os.makedirs(dst)
        png_files = [filename for filename in os.listdir(src_dir_win) if filename.endswith('.png')]
        for filename in png_files:
            shutil.copy(os.path.join(src_dir_win, filename), dst)
        with open(os.path.join(dst, 'dunngen.ini'), 'w') as f:
            f.write("[images]\nforce_sprites=YES\n\n[sprite]\nftime=20 fps\natime=3000000")

    def create_symonoff(self, sym, src_dir):
        self.create_symnonwin(sym, src_dir)

        dst = os.path.join(self.__res_dir__, self.sym_dir_, sym, 'win')
        if not os.path.exists(dst):
            os.makedirs(dst)
        with open(os.path.join(dst, sym+'_000.png.link'), 'w') as f:
            f.write('"/symbol/{0}/{1}.png"'.format(sym, sym))
        with open(os.path.join(dst, sym+'_001.png.link'), 'w') as f:
            f.write('"/common/shared/other/transparent.png"')
        with open(os.path.join(dst, 'dunngen.ini'), 'w') as f:
            f.write("[images]\nforce_sprites=YES\n\n[sprite]\nftime=2 fps\natime=3000000")
            
    ############################################
    # sym_name is the source file name
    ############################################
    def create_symnonwin_custom(self, sym, src_dir, sym_name=None, parent_sym=None):
        if sym_name is None:
            sym_name = sym
            
        dst = os.path.join(self.__res_dir__, self.sym_dir_, parent_sym, sym, 'nonwin')
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copy(os.path.join(src_dir, sym_name+'.png'), dst)
        with open(os.path.join(dst, 'dunngen.ini'), 'w') as f:
            f.write("[images]\nforce_sprites=YES\n\n[sprite]\nftime=2 fps\natime=3000000")
            
            
    def create_symonoff_custom(self, sym, src_dir, sym_name=None, parent_sym=None):
        self.create_symnonwin_custom(sym, src_dir, sym_name, parent_sym)

        if sym_name is None:
            sym_name = sym
            
        dst = os.path.join(self.__res_dir__, self.sym_dir_, parent_sym, sym, 'win')
        if not os.path.exists(dst):
            os.makedirs(dst)
            
        with open(os.path.join(dst, sym_name+'_000.png.link'), 'w') as f:
            f.write('"/symbol/{0}/{1}.png"'.format(sym, sym))
        with open(os.path.join(dst, sym_name+'_001.png.link'), 'w') as f:
            f.write('"/common/shared/other/transparent.png"')
        with open(os.path.join(dst, 'dunngen.ini'), 'w') as f:
            f.write("[images]\nforce_sprites=YES\n\n[sprite]\nftime=2 fps\natime=3000000")
            
    # sym is diretory name        
    def create_symblock(self, sym, src_dir, sym_name=None):        

        if sym_name is None:
            sym_name = sym
            
        src_dir_new = os.path.join(src_dir, sym)
            
        #single
        sym_name_new = sym_name + '_head_only'
        self.create_symonoff_custom('single', src_dir_new, sym_name_new, sym)

        #top
        sym_name_new = sym_name + '_1'
        self.create_symonoff_custom('top', src_dir_new, sym_name_new, sym)
        
        #middle
        sym_name_new = sym_name + '_2'
        self.create_symonoff_custom('middle', src_dir_new, sym_name_new, sym)
        
        #bottom
        sym_name_new = sym_name + '_3'
        self.create_symonoff_custom('bottom', src_dir_new, sym_name_new, sym)
