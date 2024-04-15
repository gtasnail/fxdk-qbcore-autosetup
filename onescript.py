import json
import os
import shutil
import subprocess
import requests
import zipfile
import time
import errno
import stat


def download_file(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content) # :shrug:

def unzip_file(src, dest, extra, strip_top_folder=False):
    with zipfile.ZipFile(src, 'r') as zip_ref:
        if not strip_top_folder:
            zip_ref.extractall(extra)
        else: # i hate this but yeah
            members = zip_ref.namelist()
            top_folder = os.path.commonprefix(members)
            for member in members:
                target_path = os.path.join(extra, os.path.relpath(member, top_folder))
                if member.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
        update_assets_config('./fxproject.json', dest, True)
        
def download_github(src, ref, dest, subpath=None):
    if subpath:
        full_src = f'{src}/archive/{ref}.zip'
        zip_path = f'{dest}.zip'
        response = requests.get(full_src)
        with open(zip_path, 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            subpath_prefix = f'{src.split("/")[-1]}-{ref}/{subpath}/'
            for member in zip_ref.namelist():
                if member.startswith(subpath_prefix):
                    zip_ref.extract(member, dest)
        os.remove(zip_path) 
        subpath_dir = os.path.join(dest, f'{src.split("/")[-1]}-{ref}', subpath) #hackyith9000
        for item in os.listdir(subpath_dir):
            shutil.move(os.path.join(subpath_dir, item), dest)
        shutil.rmtree(os.path.join(dest, f'{src.split("/")[-1]}-{ref}'), ignore_errors=True)
    else:
        subprocess.run(['git', 'clone', '--branch', ref, '--single-branch', src, dest])


def onerror(func, path, exc_info):
    excvalue = exc_info[1]
    if excvalue.errno == errno.EACCES or excvalue.winerror == 32:
        os.chmod(path, stat.S_IWUSR)  # stupid fucking shit fuck hate it >:( basically grant write access
        try:
            func(path)
        except PermissionError: # raaaaaaaa 
            pass  
    else:
        raise excvalue
    
def update_assets_config(cfg_path, asset_path, enabled=True):
    standardized_path = asset_path.replace('/', '\\')  
    if standardized_path not in ('[cfx-default]', '[standalone]', '.\\.fxdk\\fxserver\\blank.cfg'):
        with open(cfg_path, 'r+') as file:
            config = json.load(file)
            assets = config.get('assets', {})
            assets[standardized_path] = {"enabled": enabled}
            config['assets'] = assets
            file.seek(0)
            json.dump(config, file, indent=2)
            file.truncate()


def clear_console():
   os.system('cls')
    
def move_path(src, dest):
    git_path = os.path.join(src, '.git')
    if os.path.exists(git_path):
        print('Removing .git directory')
        shutil.rmtree(git_path, onerror=onerror)

    update_assets_config('./fxproject.json', dest, True)
    if os.path.isdir(dest):
        shutil.rmtree(dest, onerror=onerror)
    try:
        shutil.move(src, dest)
    except PermissionError as e:
        print(f"failed to move {src} to {dest} due to locked files: {e}") # debug my brain

def configure_server_cfg(cfg_path, config_data): # meh
    with open(cfg_path, 'r') as file:
        cfg_lines = file.readlines()
        
    with open(cfg_path, 'w') as file:
        for line in cfg_lines:
            for key, value in config_data.items():
                line = line.replace(    '{{'+key+'}}', value)
            file.write(line)



def main():

    dbConnectionString = input('Enter database connection string: ')
    
    config_data = {
        'serverEndpoints': "0.0.0.0:30120",
        'maxClients': "1",
        'svLicense': 'cfx_fxdk',
        'serverName': "FXDK",
        'recipeName': "FXDK",
        'recipeAuthor': "FXDK",
        'recipeDescription': "FXDK",
        'dbConnectionString': dbConnectionString,
        'addPrincipalsMaster': 'add_ace builtin.everyone command allow'
    }
    



    # We shall download all required resources now extremely bad way to do this but :P
    download_github('https://github.com/qbcore-framework/txAdminRecipe', 'main', './tmp/qbcore')
    move_path('./tmp/qbcore/server.cfg', './.fxdk/fxserver/blank.cfg')

    download_file('https://github.com/overextended/oxmysql/releases/download/v2.8.0/oxmysql.zip', './tmp/oxmysql.zip')
    unzip_file('./tmp/oxmysql.zip', '[standalone]', '[standalone]/oxmysql', True)


    download_file('https://github.com/ThymonA/menuv/releases/download/v1.4.1/menuv_v1.4.1.zip', './tmp/menuv.zip')
    unzip_file('./tmp/menuv.zip', '[standalone]/menuv', '[standalone]/menuv')
    
    download_github('https://github.com/qbcore-framework/bob74_ipl', 'master', './tmp/bob74_ipl')
    move_path('./tmp/bob74_ipl', '[standalone]/bob74_ipl')
    
    download_github('https://github.com/qbcore-framework/safecracker', 'main', './tmp/safecracker')
    move_path('./tmp/safecracker', '[standalone]/safecracker')
    
    download_github('https://github.com/citizenfx/screenshot-basic', 'master', './tmp/screenshot-basic')
    move_path('./tmp/screenshot-basic', '[standalone]/screenshot-basic')
    
    download_github('https://github.com/qbcore-framework/progressbar', 'main', './tmp/progressbar')
    move_path('./tmp/progressbar', '[standalone]/progressbar')
    
    download_github('https://github.com/qbcore-framework/interact-sound', 'master', './tmp/interact-sound')
    move_path('./tmp/interact-sound', '[standalone]/interact-sound')
    
    download_github('https://github.com/qbcore-framework/connectqueue', 'master', './tmp/connectqueue')
    move_path('./tmp/connectqueue', '[standalone]/connectqueue')
    
    download_github('https://github.com/qbcore-framework/PolyZone', 'master', './tmp/PolyZone')
    move_path('./tmp/PolyZone', '[standalone]/PolyZone')
    
    download_github('https://github.com/qbcore-framework/LegacyFuel', 'master', './tmp/LegacyFuel')
    move_path('./tmp/LegacyFuel', '[standalone]/LegacyFuel')
    time.sleep(10)
    
    download_github('https://github.com/AvarianKnight/pma-voice', 'main', './tmp/pma-voice')
    move_path('./tmp/pma-voice', '[voice]/pma-voice')
    
    download_github('https://github.com/qbcore-framework/qb-radio', 'main', './tmp/qb-radio')
    move_path('./tmp/qb-radio', '[voice]/qb-radio')
    
    download_github('https://github.com/qbcore-framework/hospital_map', 'main', './tmp/hospital_map')
    move_path('./tmp/hospital_map', '[default_maps]/hospital_map')
    
    download_github('https://github.com/qbcore-framework/dealer_map', 'main', './tmp/dealer_map')
    move_path('./tmp/dealer_map', '[default_maps]/dealer_map')
    
    download_github('https://github.com/qbcore-framework/prison_map', 'main', './tmp/prison_map')
    move_path('./tmp/prison_map', '[defaultmaps]/[prison_map]/prison_map')
    
    time.sleep(10)
    
    download_github('https://github.com/qbcore-framework/qb-core', 'main', './tmp/qb-core')
    move_path('./tmp/qb-core', '[qb]/qb-core')
    
    download_github('https://github.com/qbcore-framework/qb-scoreboard', 'main', './tmp/qb-scoreboard')
    move_path('./tmp/qb-scoreboard', '[qb]/qb-scoreboard')
    
    download_github('https://github.com/qbcore-framework/qb-adminmenu', 'main', './tmp/qb-adminmenu')
    move_path('./tmp/qb-adminmenu', '[qb]/qb-adminmenu')
    
    download_github('https://github.com/qbcore-framework/qb-multicharacter', 'main', './tmp/qb-multicharacter')
    move_path('./tmp/qb-multicharacter', '[qb]/qb-multicharacter')
    
    download_github('https://github.com/qbcore-framework/qb-target', 'main', './tmp/qb-target')
    move_path('./tmp/qb-target', '[qb]/qb-target')
    
    download_github('https://github.com/qbcore-framework/qb-vehiclesales', 'main', './tmp/qb-vehiclesales')
    move_path('./tmp/qb-vehiclesales', '[qb]/qb-vehiclesales')
    
    download_github('https://github.com/qbcore-framework/qb-vehicleshop', 'main', './tmp/qb-vehicleshop')
    move_path('./tmp/qb-vehicleshop', '[qb]/qb-vehicleshop')
    
    download_github('https://github.com/qbcore-framework/qb-houserobbery', 'main', './tmp/qb-houserobbery')
    move_path('./tmp/qb-houserobbery', '[qb]/qb-houserobbery')
    
    download_github('https://github.com/qbcore-framework/qb-prison', 'main', './tmp/qb-prison')
    move_path('./tmp/qb-prison', '[qb]/qb-prison')
    
    download_github('https://github.com/qbcore-framework/qb-hud', 'main', './tmp/qb-hud')
    move_path('./tmp/qb-hud', '[qb]/qb-hud')
    
    download_github('https://github.com/qbcore-framework/qb-management', 'main', './tmp/qb-management')
    move_path('./tmp/qb-management', '[qb]/qb-management')
    
    download_github('https://github.com/qbcore-framework/qb-weed', 'main', './tmp/qb-weed')
    move_path('./tmp/qb-weed', '[qb]/qb-weed')
        
    download_github('https://github.com/qbcore-framework/qb-lapraces', 'main', './tmp/qb-lapraces')
    move_path('./tmp/qb-lapraces', '[qb]/qb-lapraces')
        
    download_github('https://github.com/qbcore-framework/qb-inventory', 'main', './tmp/qb-inventory')
    move_path('./tmp/qb-inventory', '[qb]/qb-inventory')
        
    download_github('https://github.com/qbcore-framework/qb-houses', 'main', './tmp/qb-houses')
    move_path('./tmp/qb-houses', '[qb]/qb-houses')
        
    download_github('https://github.com/qbcore-framework/qb-garages', 'main', './tmp/qb-garages')
    move_path('./tmp/qb-garages', '[qb]/qb-garages')
        
    download_github('https://github.com/qbcore-framework/qb-ambulancejob', 'main', './tmp/qb-ambulancejob')
    move_path('./tmp/qb-ambulancejob', '[qb]/qb-ambulancejob')
    
    time.sleep(10)
        
    download_github('https://github.com/qbcore-framework/qb-radialmenu', 'main', './tmp/qb-radialmenu')
    move_path('./tmp/qb-radialmenu', '[qb]/qb-radialmenu')
        
    download_github('https://github.com/qbcore-framework/qb-crypto', 'main', './tmp/qb-crypto')
    move_path('./tmp/qb-crypto', '[qb]/qb-crypto')
        
    download_github('https://github.com/qbcore-framework/qb-weathersync', 'main', './tmp/qb-weathersync')
    move_path('./tmp/qb-weathersync', '[qb]/qb-weathersync')
        
    download_github('https://github.com/qbcore-framework/qb-policejob', 'main', './tmp/qb-policejob')
    move_path('./tmp/qb-policejob', '[qb]/qb-policejob')
        
    download_github('https://github.com/qbcore-framework/qb-traphouse', 'main', './tmp/qb-traphouse')
    move_path('./tmp/qb-traphouse', '[qb]/qb-traphouse')
        
    download_github('https://github.com/qbcore-framework/qb-apartments', 'main', './tmp/qb-apartments')
    move_path('./tmp/qb-apartments', '[qb]/qb-apartments')
        
    download_github('https://github.com/qbcore-framework/qb-vehiclekeys', 'main', './tmp/qb-vehiclekeys')
    move_path('./tmp/qb-vehiclekeys', '[qb]/qb-vehiclekeys')
        
    download_github('https://github.com/qbcore-framework/qb-mechanicjob', 'main', './tmp/qb-mechanicjob')
    move_path('./tmp/qb-mechanicjob', '[qb]/qb-mechanicjob')
        
    download_github('https://github.com/qbcore-framework/qb-phone', 'main', './tmp/qb-phone')
    move_path('./tmp/qb-phone', '[qb]/qb-phone')
        
    download_github('https://github.com/qbcore-framework/qb-vineyard', 'main', './tmp/qb-vineyard')
    move_path('./tmp/qb-vineyard', '[qb]/qb-vineyard')
        
    download_github('https://github.com/qbcore-framework/qb-weapons', 'main', './tmp/qb-weapons')
    move_path('./tmp/qb-weapons', '[qb]/qb-weapons')
        
    download_github('https://github.com/qbcore-framework/qb-scrapyard', 'main', './tmp/qb-scrapyard')
    move_path('./tmp/qb-scrapyard', '[qb]/qb-scrapyard')
        
    download_github('https://github.com/qbcore-framework/qb-towjob', 'main', './tmp/qb-towjob')
    move_path('./tmp/qb-towjob', '[qb]/qb-towjob')
            
    download_github('https://github.com/qbcore-framework/qb-streetraces', 'main', './tmp/qb-streetraces')
    move_path('./tmp/qb-streetraces', '[qb]/qb-streetraces')
            
    download_github('https://github.com/qbcore-framework/qb-storerobbery', 'main', './tmp/qb-storerobbery')
    move_path('./tmp/qb-storerobbery', '[qb]/qb-storerobbery')
            
    download_github('https://github.com/qbcore-framework/qb-spawn', 'main', './tmp/qb-spawn')
    move_path('./tmp/qb-spawn', '[qb]/qb-spawn')
            
    download_github('https://github.com/qbcore-framework/qb-smallresources', 'main', './tmp/qb-smallresources')
    move_path('./tmp/qb-smallresources', '[qb]/qb-smallresources')
            
    download_github('https://github.com/qbcore-framework/qb-recyclejob', 'main', './tmp/qb-recyclejob')
    move_path('./tmp/qb-recyclejob', '[qb]/qb-recyclejob')
            
    download_github('https://github.com/qbcore-framework/qb-diving', 'main', './tmp/qb-diving')
    move_path('./tmp/qb-diving', '[qb]/qb-diving')
            
    download_github('https://github.com/qbcore-framework/qb-cityhall', 'main', './tmp/qb-cityhall')
    move_path('./tmp/qb-cityhall', '[qb]/qb-cityhall')
            
    download_github('https://github.com/qbcore-framework/qb-truckrobbery', 'main', './tmp/qb-truckrobbery')
    move_path('./tmp/qb-truckrobbery', '[qb]/qb-truckrobbery')
            
    download_github('https://github.com/qbcore-framework/qb-pawnshop', 'main', './tmp/qb-pawnshop')
    move_path('./tmp/qb-pawnshop', '[qb]/qb-pawnshop')
            
    download_github('https://github.com/qbcore-framework/qb-minigames', 'main', './tmp/qb-minigames')
    move_path('./tmp/qb-minigames', '[qb]/qb-minigames')
            
    download_github('https://github.com/qbcore-framework/qb-taxijob', 'main', './tmp/qb-taxijob')
    move_path('./tmp/qb-taxijob', '[qb]/qb-taxijob')
            
    download_github('https://github.com/qbcore-framework/qb-busjob', 'main', './tmp/qb-busjob')
    move_path('./tmp/qb-busjob', '[qb]/qb-busjob')
            
    download_github('https://github.com/qbcore-framework/qb-newsjob', 'main', './tmp/qb-newsjob')
    move_path('./tmp/qb-newsjob', '[qb]/qb-newsjob')
            
    download_github('https://github.com/qbcore-framework/qb-jewelery', 'main', './tmp/qb-jewelery')
    move_path('./tmp/qb-jewelery', '[qb]/qb-jewelery')
            
    download_github('https://github.com/qbcore-framework/qb-bankrobbery', 'main', './tmp/qb-bankrobbery')
    move_path('./tmp/qb-bankrobbery', '[qb]/qb-bankrobbery')
            
    download_github('https://github.com/qbcore-framework/qb-truckerjob', 'main', './tmp/qb-truckerjob')
    move_path('./tmp/qb-truckerjob', '[qb]/qb-truckerjob')
            
    download_github('https://github.com/qbcore-framework/qb-fitbit', 'main', './tmp/qb-fitbit')
    move_path('./tmp/qb-fitbit', '[qb]/qb-fitbit')
            
    download_github('https://github.com/qbcore-framework/qb-banking', 'main', './tmp/qb-banking')
    move_path('./tmp/qb-banking', '[qb]/qb-banking')
                
    download_github('https://github.com/qbcore-framework/qb-clothing', 'main', './tmp/qb-clothing')
    move_path('./tmp/qb-clothing', '[qb]/qb-clothing')
                
    download_github('https://github.com/qbcore-framework/qb-hotdogjob', 'main', './tmp/qb-hotdogjob')
    move_path('./tmp/qb-hotdogjob', '[qb]/qb-hotdogjob')
                
    download_github('https://github.com/qbcore-framework/qb-doorlock', 'main', './tmp/qb-doorlock')
    move_path('./tmp/qb-doorlock', '[qb]/qb-doorlock')
                
    download_github('https://github.com/qbcore-framework/qb-garbagejob', 'main', './tmp/qb-garbagejob')
    move_path('./tmp/qb-garbagejob', '[qb]/qb-garbagejob')
                
    download_github('https://github.com/qbcore-framework/qb-drugs', 'main', './tmp/qb-drugs')
    move_path('./tmp/qb-drugs', '[qb]/qb-drugs')
                
    download_github('https://github.com/qbcore-framework/qb-shops', 'main', './tmp/qb-shops')
    move_path('./tmp/qb-shops', '[qb]/qb-shops')
                
    download_github('https://github.com/qbcore-framework/qb-interior', 'main', './tmp/qb-interior')
    move_path('./tmp/qb-interior', '[qb]/qb-interior')
                
    download_github('https://github.com/qbcore-framework/qb-menu', 'main', './tmp/qb-menu')
    move_path('./tmp/qb-menu', '[qb]/qb-menu')
    time.sleep(10)
                    
    download_github('https://github.com/qbcore-framework/qb-loading', 'main', './tmp/qb-loading')
    move_path('./tmp/qb-loading', '[qb]/qb-loading')

    shutil.rmtree('./tmp', ignore_errors=True) # we cleanup 
        
    clear_console()
    configure_server_cfg('.fxdk/fxserver/blank.cfg', config_data)

    
    

if __name__ == "__main__":
    main()
