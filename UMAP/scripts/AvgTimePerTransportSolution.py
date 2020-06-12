import sys
sys.path.append('../..')
import matplotlib.pyplot as plt

class AvgTimePerTransportSolution:

    def __init__(self, config, rentals, save=False):


        rentals = rentals[(rentals.pt_duration != -1) &
                          (rentals.pt_duration < 60*60*24)
                          ]


        pt = rentals.groupby('Hour').mean()['pt_duration'].div(60)
        driving = rentals.groupby('Hour').mean()['driving_duration'].div(60)
        c2g = rentals[rentals.vendor== 'car2go']
        c2g = c2g.groupby('Hour').mean()['duration'].div(60)
        enj = rentals[rentals.vendor== 'enjoy']
        enj = enj.groupby('Hour').median()['duration'].div(60)
        print(enj)

        fig, ax = plt.subplots(figsize=config['figsize'])

        ax.plot(pt, color=config['colors']['pt'], label='PT')
        ax.plot(driving, color=config['colors']['driving'], label='Driving')
        ax.plot(c2g, color=config['colors']['car2go'], label='Car2go')
        ax.plot(enj, color=config['colors']['enjoy'], label='Enjoy')
        
        ax.set_xticks(pt.index)


        ax.legend()
        ax.grid()

        fig.show()


