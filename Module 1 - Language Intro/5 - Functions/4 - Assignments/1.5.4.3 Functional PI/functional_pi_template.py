import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###

    pi_estimate = 0.0
    counter = 0

    a = 1
    b = 1 / math.sqrt(2)
    t = 1 / 4
    p = 1

    while (abs(pi_estimate - math.pi)) > target_error:
        """
        Step 2: Update each variable based upon the algorithm. Take care to ensure
        the order of operations and dependencies among calculations is respected. You
        may wish to create new "temporary" variables to hold intermediate results
        """

        ### YOUR CODE HERE ###

        a_n = (a + b) / 2
        b_n = math.sqrt(a * b)
        t_n = t - p * pow((a - a_n), 2)
        p_n = 2 * p

        a = a_n
        b = b_n
        t = t_n
        p = p_n

        pi_estimate = pow((a + b), 2) / (4 * t)
        counter += 1

    # change this so an actual value is returned
    print("Loops: " + str(counter))
    return pi_estimate


desired_error = 1e-2

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
