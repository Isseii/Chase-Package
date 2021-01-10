import random
import json
import csv
import logging
import os
import configparser
from pathlib import Path
from chase.sheep import Sheep
from chase.wolf import Wolf


class Simulation:


    def __init__(self,rounds, sheep_number, wait, directory, conf):
        if conf != False and self.__configuration(conf) != -1:
            Sheep.sheep_move_dist, Sheep.init_pos_limit,  Wolf.wolf_move_dist = self.__configuration(conf)
        self.__simulation(rounds, sheep_number, wait, directory)



    def __configuration(self,conf_file):
        if not Path(conf_file).is_file():
            logging.error("Configuration file with path " + conf_file + " doesn't exist!")
            return -1
        config = configparser.ConfigParser()
        config.read(conf_file)
        smove, ini, wmove = float(config.get('Movement', 'SheepMoveDist')), float(
             config.get('Terrain', 'InitPosLimit')), float(config.get('Movement', 'WolfMoveDist'))
        if (smove > 0 and ini > 0 and wmove > 0):
            logging.debug(
            "_configuration called with argument(" + str(conf_file) + " ), returned (" + str(smove) + "," +  str(ini) + "," +   str(wmove) +  ")")
            return smove, ini, wmove
        logging.error("Negative value passed to configuration file!")
        raise ("Incorrect value in configuration file!")



    def __to_json(self,sheep_arr, wolf, data, i):
        sheeps_holder = []
        for j in range(len(sheep_arr)):
            pos = str(sheep_arr[j].xPos) + " " + str(sheep_arr[j].yPos)
            sheeps_holder.append(pos)
        pos = str(round(wolf.xPos, 3)) + " " + str(round(wolf.yPos, 3))
        data['lea'].append({'round_no': i,
                            'wolf_pos': pos,
                            'sheep_pos': sheeps_holder})
        logging.debug("__toJson called with argument("+ str(sheep_arr) + "," + str(wolf) + ","+ str(data) + "," + str(i) +" ), returned ("+ str(data) +")")
        return data


    def __to_csv(self,sheeps,directory):
        path = os.path.join(directory ,'alive.csv')
        try:
            if os.path.getsize(path) > 0:
                logging.warning("Json file was not empty!")
        except FileNotFoundError:
            logging.debug("Creating CSV file!")

        logging.debug("__toCsv called with argument("+ str(sheeps) + "," + directory +" )")
        with open(path, 'w+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Round', 'Sheeps_Alive'])
            round = 0
            for s in sheeps:
                writer.writerow([round, s])
                round += 1


    def __generate_sheeps(self,no):
        sheep_arr = []
        for i in range(0, no):
            posx = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
            posy = (random.randrange(-(2 * Sheep.init_pos_limit), (2 * Sheep.init_pos_limit) + 1, 1)) / 2
            sheep_arr.append(Sheep(posx, posy, logging))
        logging.debug(
            "__generate_sheeps called with argument(" + str(no) +  " ), returned (" + str(sheep_arr) + ")")
        return sheep_arr


    def __simulation(self,rounds, sheep_number, wait, directory):
        logging.debug(
            " __simulation called with argument(" + str(rounds) + "," +  str(sheep_number) + "," +  str(wait) + "," +   str(directory) + ")")
        log = ("Round number ", 0)
        logging.info(log)
        sheep_arr = self.__generate_sheeps(sheep_number)
        wolf = Wolf(logging)
        data = {}
        sheeps_alive = []
        data['lea'] = []
        self.__to_json(sheep_arr, wolf, data, 0)
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
            self.__to_json(sheep_arr, wolf, data, i + 1)
            sheeps_alive.append(wolf.alive_sheeps)
            if wolf.alive_sheeps == 0:
                break
        path = os.path.join(directory, 'pos.json')
        try:
            if os.path.getsize(path) > 0:
                logging.warning("Json file was not empty!")
        except FileNotFoundError:
            logging.debug("Creating Json file!")
        self.__to_csv(sheeps_alive, directory)
        with open(path, 'w+') as outfile:
            json.dump(data, outfile, indent=2)


