import random
import json
import argparse
import csv
import logging
import os
import configparser
from argparse import RawTextHelpFormatter
from pathlib import Path
from sheep import Sheep
from wolf import Wolf


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s value must be positive" % value)
    logging.debug("check_positive(", value, ") called, returned,", ivalue)
    return ivalue


def __setup():
    Sheep.init_pos_limit = 10.0
    Sheep.sheep_move_dist = 0.5
    Wolf.wolf_move_dist = 1.0
    sheep_number = 15
    rounds = 50
    directory = os.path.dirname(os.path.realpath(__file__))
    wait = False
    parser = argparse.ArgumentParser(description='Wolf hunting sheeps simulation. \n\n'
                                                 'Wolf moves in straight line towards nearest sheep in attempt to kill her. \n'
                                                 'Sheeps move each time in one of four directions randomly choosen '
                                                 'from UP,DOWN,LEFT,RIGHT.\n'
                                                 'Every animal moves once per round. \n'
                                                 'Simulation ends with last round or death of last sheep.' ,formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--config', help="Allows you to choose configuration file.",
                        action='store', dest='conf', metavar='FILE')
    parser.add_argument('-d', '--dir', action='store', help="Choose where to save json and csv files", dest='directory',
                        metavar='DIR')
    parser.add_argument('-l', '--log', action='store',
                        help="Create log file with log LEVEL (INFO,DEBUG,WARNING,ERROR,CRITICAL)", dest='log_lvl',
                        metavar='LEVEL')
    parser.add_argument('-r', '--rounds', action='store',
                        help="Allows you to specify number of rounds simulation should last for.", dest='rounds',
                        type=check_positive, metavar='NUM')
    parser.add_argument('-s', '--sheep', action='store', help="Allows your to specify number of sheeps in simulation.",
                        dest='sheep_number',
                        type=check_positive, metavar='NUM')
    parser.add_argument('-w', '--wait', action='store_true', help="Wait for Enter key after each round!")
    args = parser.parse_args()
    if args.log_lvl:
        with open('chase.log', 'w'):
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
        logging.basicConfig(level=lvl, filename="chase.log")
        logging.debug("debug")
    if args.conf:
        if __configuration(args.conf) != -1:
            Sheep.sheep_move_dist, Sheep.init_pos_limit, Wolf.wolf_move_dist = __configuration(args.conf)
    if args.directory:
        directory = args.directory
    if args.rounds:
        rounds = args.rounds
    if args.sheep_number:
        sheep_number = args.sheep_number
    if args.wait:
        wait = args.wait
    __simulation(rounds, sheep_number, wait, directory)


def __configuration(conf_file):
    if not Path(conf_file).is_file():
        logging.error("Configuration file with path " + conf_file + " doesn't exist!")
        return -1

    config = configparser.ConfigParser()
    config.read(conf_file)
    smove, ini, wmove = float(config.get('Movement', 'SheepMoveDist')), float(
         config.get('Terrain', 'InitPosLimit')), float(config.get('Movement', 'WolfMoveDist'))
    if (smove > 0 and ini > 0 and wmove > 0):
        return smove, ini, wmove
    logging.error("Negative value passed to configuration file!")
    raise ("Incorrect value in configuration file!")





def __toJson(sheep_arr, wolf, data, i):
    sheeps_holder = []
    for j in range(len(sheep_arr)):
        pos = str(sheep_arr[j].xPos) + " " + str(sheep_arr[j].yPos)
        sheeps_holder.append(pos)
    pos = str(round(wolf.xPos, 3)) + " " + str(round(wolf.yPos, 3))
    data['lea'].append({'round_no': i,
                        'wolf_pos': pos,
                        'sheep_pos': sheeps_holder})
    return data


def __toCsv(sheeps,directory):
    path = os.path.join(directory ,'alive.csv')
    if os.path.getsize(path) > 0:
        logging.warning("CSV file was not empty!")
    with open(path, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Round', 'Sheeps_Alive'])
        round = 0
        for s in sheeps:
            writer.writerow([round, s])
            round += 1


def __generate_sheeps(no):
    sheep_arr = []
    for i in range(0, no):
        posx = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
        posy = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
        sheep_arr.append(Sheep(posx, posy, logging))
    return sheep_arr


def __simulation(rounds, sheep_number, wait, directory):
    log = ("Round number ", 0)
    logging.info(log)
    sheep_arr = __generate_sheeps(sheep_number)
    wolf = Wolf(logging)
    data = {}
    sheeps_alive = []
    data['lea'] = []
    __toJson(sheep_arr, wolf, data, 0)
    sheeps_alive.append(sheep_number)
    print(log)
    log = "Wolf Position  X : ", round(wolf.xPos, 3), ", Y :", round(wolf.yPos, 3)
    logging.info(log)
    print(log)
    log = "Number of sheeps alive ", sheep_number
    logging.info(log)
    print(log)
    for i in range(rounds):
        log = ("Round number ", i + 1)
        logging.info(log)
        if (wait):
            input("Press enter to continue...")
        print("Round : ", i + 1)
        for j in range(len(sheep_arr)):
            sheep_arr[j].move()
            pos = "Position of sheep nr:", j, " X: ", sheep_arr[j].xPos, "Y: ", sheep_arr[j].yPos
            logging.info(pos)
        wolf.move(sheep_arr)
        pos = str(wolf.xPos) + " " + str(wolf.yPos)
        log = "Wolf Position  X : ", round(wolf.xPos, 3), ", Y :", round(wolf.yPos, 3)
        logging.info(log)
        print(log)
        if wolf.killed_sheep != -1:
            log = ("Wolf killed sheep number ", wolf.killed_sheep)
            logging.info(log)
            print(log)
        log = ("Number of sheeps alive ", wolf.alive_sheeps)
        logging.info(log)
        print(log)
        __toJson(sheep_arr, wolf, data, i + 1)
        sheeps_alive.append(wolf.alive_sheeps)
        if wolf.alive_sheeps == 0:
            break

    path = os.path.join(directory, 'pos.json')
    if not os.path.exists(directory):
        os.makedirs(directory)
    elif   os.path.getsize(path) > 0:
        logging.warning("Json file was not empty!")


    __toCsv(sheeps_alive, directory)
    with open(path, 'w+') as outfile:
        json.dump(data, outfile, indent=2)


if __name__ == "__main__":
    __setup()
