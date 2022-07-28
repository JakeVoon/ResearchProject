import from_wavelength
import from_positions
import matplotlib.pyplot as plt

data_idx = 15

if __name__ == '__main__':
    thetas_from_wavelength = from_wavelength.main(data_idx)
    thetas_from_positions = from_positions.main(data_idx)
    diff = thetas_from_wavelength - thetas_from_positions

    plt.plot(thetas_from_wavelength)
    plt.plot(thetas_from_positions)
    plt.plot(diff)

    plt.show()
