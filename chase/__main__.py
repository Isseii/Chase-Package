import os
import argparse
import logging
from pathlib import Path
from  chase.simulation import Simulation
from argparse import RawTextHelpFormatter

def __setup():
    sheep_number = 15
    rounds = 50
    conf = False
    directory = os.path.dirname(os.path.realpath(__file__))
    wait = False
    lvl = 0

    parser = argparse.ArgumentParser(description='Wolf hunting sheeps simulation. \n\n'
                                                 'Wolf moves in straight line towards nearest sheep in attempt to kill her. \n'
                                                 'Sheeps move each time in one of four directions randomly choosen '
                                                 'from UP,DOWN,LEFT,RIGHT.\n'
                                                 'Every animal moves once per round. \n'
                                                 'Simulation ends with last round or death of last sheep.',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--config', help="Allows you to choose configuration file.",
                        action='store', dest='conf', metavar='FILE')
    parser.add_argument('-d', '--dir', action='store', help="Choose where to save json, csv and log files", dest='directory',
                        metavar='DIR')
    parser.add_argument('-l', '--log', action='store',
                        help="Create log file with log LEVEL (INFO,DEBUG,WARNING,ERROR,CRITICAL)", dest='log_lvl',
                        metavar='LEVEL')
    parser.add_argument('-r', '--rounds', action='store',
                        help="Allows you to specify number of rounds simulation should last for.", dest='rounds',
                        type=int, metavar='NUM')
    parser.add_argument('-s', '--sheep', action='store', help="Allows your to specify number of sheeps in simulation.",
                        dest='sheep_number',
                        type=int, metavar='NUM')
    parser.add_argument('-w', '--wait', action='store_true', help="Wait for Enter key after each round!")
    args = parser.parse_args()
    if args.directory:
        directory = args.directory
        if not os.path.exists(directory):
            os.makedirs(directory)
    if args.log_lvl:
        path = os.path.join(directory, 'chase.log')
        with open(path, 'w'):
            pass
        if args.log_lvl == "INFO":
            lvl = logging.INFO
        elif args.log_lvl == "DEBUG":
            lvl = logging.DEBUG
        elif args.log_lvl == "WARNING":
            lvl = logging.WARNING
        elif args.log_lvl == "ERROR":
            lvl = logging.ERROR
        elif args.log_lvl == "CRITICAL":
            lvl = logging.CRITICAL
        else:
            raise ValueError("Invalid log level!")
        path = os.path.join(directory, 'chase.log')
        logging.basicConfig(level=lvl, filename=path)
    if args.conf:
        conf = args.conf
    if args.rounds:
        __check_positive(args.rounds)
        rounds = args.rounds
    if args.sheep_number:
        __check_positive(args.sheep_number)
        sheep_number = args.sheep_number
    if args.wait:
        wait = args.wait

    logging.debug("Simulation() called ")

    Simulation(rounds, sheep_number, wait, directory, conf)


def __check_positive(value):
    ivalue = int(value)
    logging.debug("check_positive(" +  str(value) +  ") called, returned," + str(ivalue))
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s value must be positive" % value)
    return ivalue


if __name__ == "__main__":
    # execute only if run as a script
    __setup()