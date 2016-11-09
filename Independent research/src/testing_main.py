import modular_prob_dist

def main():

    # compute_prob(xo=0, yo=0, sd=100)
    # Create a sample listener and controller
    listener = modular_prob_dist.SampleListener()
    controller = modular_prob_dist.Leap.Controller()


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)


    # Starts plot on run

    modular_prob_dist.calculations().average_center()
    prob = modular_prob_dist.calculations().compute_prob(xo=modular_prob_dist.avg_xpar_sum, yo=modular_prob_dist.avg_ypar_sum - 200, sd=100)
    print modular_prob_dist.np.round(prob, 6)
    print
    print'sum of prob = %f' % prob.sum()
    modular_prob_dist.plt.pcolor(prob[::-1, :])
    modular_prob_dist.plt.axes().set_aspect('equal')
    controller.remove_listener(listener)
    modular_prob_dist.plt.show()




#-----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
