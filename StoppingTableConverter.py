import os.path as path                                                #Required for dealing with file path

START_STR = "-----------  ---------- ---------- ----------  ----------  ----------"  #Change when dealing with multiple atom types
END_STR = "-----------------------------------------------------------"              #

def CleanFile(InputFile, Path = ""):
    File = open(path.join(Path, InputFile)).read().split("\n")

    Start_Index = File.index(START_STR)                               #Gets index based on the string, must change to account for multiple atom types 
    Stop_Index = File.index(END_STR)

    File =  File[Start_Index+1:Stop_Index]
    IonEnergy = []
    IonEnergyUnits = []
    dE_dx_Electron = []
    dE_dx_Nuclear = []
    for i in range(len(File)):
        File[i] = File[i].split()
        IonEnergy.append(float(File[i][0]))
        IonEnergyUnits.append(File[i][1])
        dE_dx_Electron.append(eval(File[i][2]))                      #Evaluates exponsents in value
        dE_dx_Nuclear.append(eval(File[i][2]))

        if IonEnergyUnits[i] == "keV":                               #Corrects value w.r.t. units
            IonEnergy[i] = IonEnergy[i]*10**3
        elif IonEnergyUnits[i] == "MeV":
            IonEnergy[i] = IonEnergy[i]*10**6
    

    return IonEnergy, IonEnergyUnits, dE_dx_Electron, dE_dx_Nuclear

def ElectronStoppingClean(InputFile, Path = ""):                    #Use if Electron Stopping Table is needed eg. fix electron/stopping
    IonEnergy, IonEnergyUnits, dE_dx_Electron, dE_dx_Nuclear = CleanFile(InputFile, Path)
    OutputFile = InputFile.split(".")[0] + "ElectronStopping.txt"
    IonEnergy.insert(0, "#Ion Energy (eV)")
    dE_dx_Electron.insert(0, "#Electron Stopping dE/dX (eV/Angstrom)")

    with open(path.join(Path, OutputFile), "w") as file:            
        file.write("#Electron Stopping Power Table from SRIM\n")
        file.write("#Units: Metal\n")
        for i in range(len(IonEnergy)):
            file.write(str(IonEnergy[i]) + " " + str(dE_dx_Electron[i]) + "\n")           

def NuclearStoppingClean(InputFile, Path = ""):                    #Use if Nuclear Stopping Table is needed
    IonEnergy, IonEnergyUnits, dE_dx_Electron, dE_dx_Nuclear = CleanFile(InputFile, Path)
    OutputFile = InputFile.split(".")[0] + "NuclearStopping.txt"
    IonEnergy.insert(0, "#Ion Energy (eV)")
    dE_dx_Nuclear.insert(0, "#Nuclear Stopping dE/dX (eV/Angstrom)")

    with open(path.join(Path, OutputFile), "w") as file:
        file.write("#Nuclear Stopping Power Table from SRIM\n")
        file.write("#Units: Metal\n")
        for i in range(len(IonEnergy)):
            file.write(str(IonEnergy[i]) + " " + str(dE_dx_Nuclear[i]) + "\n")
    

