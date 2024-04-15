# [FxDK](https://docs.fivem.net/docs/fxdk/) QBCore auto setup script/application

*Built with pylauncher*

## What does this do?
* Setup QBCore framework in one click
* That's pretty much it

### It handles the auto starting of each script within you're FXDK Enviroment so you don't need to manually start each resource
```
                                         #((((/                                                     
                                   ((((((((((((((((((         ,((((((((,                            
                                ((((((((((@@@@@@@@@&((((  ((((((((((((((((((                        
                              ((((((((@@@@@@@@@@@@@@@@@((((((((@@@@@@@@@@@@%((                      
                             (((((((@@@@@@@@,,,,,,,,,,,@@((((@@@@@@@*,,,,,,,@@((                    
                            (((((((@@@@@@@,,,,,,,,,,,,,,,@(#@@@@@@,,,,,,,,,,,,/(%                   
             ,(((((((((((((((((((((@@@@@@,,,,,,,,,,,,,,,,#@(@@@@@,,,,,,,,,,,,,,&(                   
        ((((((((((((((((((((((((((#@@@@@@,,,,,,,,,,,,,,,,*@(@@@@@,,,,,,,,,,,,,,#(                   
    (((((((((((((((((((((((((((((((@@@@@@#,,,,,,,,,,,,,,,@(@@@@@@@,,,,,,,,,,,,,(                    
 (((((((((((((((((((((((((((((((((((@@@@@@@,,,,,,,,,,,,@@#(((@@@@@@@,,,,,,,,/@(                     
((((((((((((((((((((((((((((((((((((((@@@@@@@@@*,,,@@@@@(((((((@@@@@@@@@@@@@(#                      
(((((/****/((((((((((((((((((((((((((((((@@@@@@@@@@@&((    ((((((((((((((((                         
((((((((((****((((((((((((((((((((((((((((((((((((((#         (((((                                 
(((((((((((((****(((((((((((((((((((((((((((((((((((((((((((((((((                                  
(((((((((((((((***/(((((((((((((((((((((((((((((((((((((((((((((((((                                
(((((((((((((((((***((((((((((((((((((((((((((((((((((((((((((((((((((                              
***(((((((((((((((***(((((((((((((((((((((((((((((((((((((((((((((((((////////                      
(****/(((((((((((((***((((((((((((((((((((((((((((((((((((((((((///,,,,,,,//   FXDK IS COOL! USE IT!                    
(((****((((((((((((/***((((((((((((((((((((((((((((((((((((((((//,,,,,,,//(                         
(((((***((((((((((((***((((((((((((((((((((((((((((((((((((((((((///,,,////.                        
((((((***(((((((((((/**/(((((((((((((((((((((((((((((((((((((((((((///////((                        
((((((/***(((((((((((***(((((((((((((((////((((((////((((((((((((((((((((((((                       
(((((((***(((((((((((***((((((((((((((//////((((/////((((((((((((((((((((((((                       
(((((((***(((((((((((***((((((((((((((///////((((///(((((((((((((((((((((((((                       
((((((***((((((((((((**((((((((((((((////////((((((((((((((((((((((((((((((((                       
(((((***((((((((((((/**(((((((((((((/////////((((((((((((((((((((((((((((((((                       
(((***/(((((((((((((**(((((((((((((/////////(((((((((((((((((((((((((((((((((                       
****(((((((((((((((/**((((((((((((/////////((((((((((((((((((((((((((((((((((                       
(((((((((((((((((((**((((((((((((((///////((((//((((((((((((((((((((((((((((                        
((((((((((((((((((**((((((((((((((((((((((((//////((((((((((((((((((((((((((                        
((((((((((((((((((/(((((((((((((((((((((((((//////(((((((((((((((((((((((((                         
((((((((((((((((((((((((((((((((((((((((((((//////(((((((((((((((((((((((((                         
(((((((((((((((((((((((((((((//////((((((((((((/((((((((((((((((((((((((((                          
  ((((((((((((((((((((((((((////////(((((((((((((((((((((((((((((((((((((                           
(((((((((((((((((((((((((((((///////(((((((((((((((((((((((((((((((((((                             
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((                              
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((                                
```

# How do i use this?
## Simply download the latest [Release](https://github.com/gtasnail/fxdk-qbcore-autosetup/releases) (Recommended)



### #1 Go into FXDK make your project and note down the location of where you made it
![image](https://github.com/gtasnail/fxdk-qbcore-autosetup/assets/100861025/d825f93d-02ca-4260-b569-6911e1266395)

### #2 Go into your projects folder (In file explorer) 
![image](https://github.com/gtasnail/fxdk-qbcore-autosetup/assets/100861025/126bf5bf-9089-4ad8-a32a-c6e0f448038a)

### #3 `Drag the fxdk-auto-qbcore.exe into your project folder (see image above of where you should put it there should be an fxproject.json in the same folder)`
![image](https://github.com/gtasnail/fxdk-qbcore-autosetup/assets/100861025/ced3befb-7ca7-44b9-8a01-0c470fe861f8)

### #4 Close FXDK and run the fxdk-auto-qbcore.exe 
![image](https://github.com/gtasnail/fxdk-qbcore-autosetup/assets/100861025/6d16e96d-2f51-48d6-9d95-724659dc4dba)

## #5 It will ask for your database connection string
You'll need to create this before hand go to 
https://github.com/qbcore-framework/txAdminRecipe/blob/main/qbcore.sql
and insert this into your database

## #6 Provide your Database string for example (mysql://root@localhost/RPThing?charset=utf8mb4)
![image](https://github.com/gtasnail/fxdk-qbcore-autosetup/assets/100861025/e4fd59a4-5538-48d9-b361-8e9aaa0bbab9)

## #7 Simply press enter and let it do it's thing once the program closes that's it setup you can start fxdk




# Alternative (the smarty pants way)
Simply run the `onescript.py` while its in your projects folder same steps as above apart from you install requirements and `cmd py onescript.py`
