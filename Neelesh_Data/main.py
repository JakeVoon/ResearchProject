import Cosserat as CRM
import numpy as np
import json
import matplotlib
import matplotlib.pyplot as plt
from scipy import integrate

if __name__=="__main__":
    # 0.5N run1
    # 1N run2
    # 1.5N run2
    # 2N run4
    # 2.5N run5

    file_name = "0.5N_run1.json"

    # Importing data
    with open(file_name) as json_file:
        run_data = json.load(json_file)

    # Saving relevant variables
    wave0 = run_data["experiment_parameters"]["wav0"]
    wave_data = run_data["data"][0]["wav_data"]
    illumisense_curvatures = np.array(run_data["data"][0]['curvatures'])

    model = CRM.CosseratRodModel(wave0,wave_data)

    plt.figure()

    m = model.get_n()    
    
    plt.figure()
    matplotlib.rcParams.update({'font.size': 15})

    plt.subplot(3,2,1)
    plt.plot(illumisense_curvatures[10:18])
    plt.title('0.5N')
    plt.xlabel('Arc length')
    plt.ylabel('Curvature')
    plt.subplot(3,2,3)
    plt.plot(m[0,:][10:18])
    plt.title('Internal moment in the x-direction')
    plt.xlabel('Arc length')
    plt.ylabel('Moment')
    plt.subplot(3,2,5)
    plt.plot(m[1,:][10:18])
    plt.title('Internal moment in the y-direction')
    plt.xlabel('Arc length')
    plt.ylabel('Moment')

#==================================================================================#

    file_name = "1N_run2.json"

    # Importing data
    with open(file_name) as json_file:
        run_data = json.load(json_file)

    # Saving relevant variables
    wave0 = run_data["experiment_parameters"]["wav0"]
    wave_data = run_data["data"][0]["wav_data"]
    illumisense_curvatures = np.array(run_data["data"][0]['curvatures'])

    model = CRM.CosseratRodModel(wave0,wave_data)

    m = model.get_m()    
    
    plt.subplot(3,2,2)
    plt.plot(illumisense_curvatures[10:18])
    plt.title('1N')
    plt.xlabel('Arc length')
    plt.ylabel('Curvature')
    plt.subplot(3,2,4)
    plt.plot(m[0,:][10:18])
    plt.title('Internal moment in the x-direction')
    plt.xlabel('Arc length')
    plt.ylabel('Moment')
    plt.subplot(3,2,6)
    plt.plot(m[1,:][10:18])
    plt.title('Internal moment in the y-direction')
    plt.xlabel('Arc length')
    plt.ylabel('Moment')
    head_title = "1N"

    plt.suptitle('Measured curvatures and internal moments with different forces applied')
    
    plt.show()

    # [10:18]
    # x = np.array(wave_data)-np.array(wave0)
    # plt.plot(x)
    # plt.axvline(x=0)
    # plt.axvline(x=25)
    # plt.axvline(x=50)
    # plt.axvline(x=75)
    # plt.axvline(x=100)

    # plt.show()

    # file_path = os.path.abspath(__file__)
    # figure = 'green rail gratings.png'

    # model = CRM.CosseratRodModel()

    # a = np.arange(25)

    # test = model.get_strain(a,a,a)

