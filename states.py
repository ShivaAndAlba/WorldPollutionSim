from __future__ import annotations

from abc import ABC, abstractmethod
from random import choice, random

import numpy as np


class State(ABC):
    """
    Interface for cell's state.
    Cell can change states according to the weather in state state.
    state change is determind by cell's neighbors from N,S,W,E
    state affect diffrently on other states
    states are described with classes Sea,Ice,Forest,Desert,City
    State change funcion:
        Sea -> Ice: if temerature drops below 0
        Ice -> Sea: if temperature goes above 0
        Forest -> Desert: if no clouds, temperature above 40
        Desert -> Forest: if clouds and temperature below 40
        City -> Desert: if temperature above 40 and pollution is max
    cities create pollution witch is scattered with the wind.
    pollution raises temperature.
    clouds are created over forests and sea, and sometimes
    drops rain witch lowers temperature and lowers pollution.
    """

    def __init__(self):
        pass

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, cell):
        self._cell = cell

    @abstractmethod
    def effect(self):
        pass

    def calculate_weather_change(self, temp_range: dict, factors: dict):
        # calculate wind change
        self.cell.wind = choice(
            [self.cell.neighbors.mean_of()["wind_mean"], choice(["N", "S", "W", "E"])]
        )

        # claculate clouds change
        if random() < self.cell.clouds:
            self.cell.clouds = 0
            self.cell.pollution = 0
            self.cell.temperature = self.cell.temperature - 1
        else:
            self.cell.clouds = self.cell.clouds + 0.4

        # calculate pollution change
        for direction, neighbor in self.cell.neighbors.everyone().items():
            if direction == "N" and neighbor.wind == "S":
                self.cell.pollution = neighbor.pollution / 2 + self.cell.pollution
            if direction == "S" and neighbor.wind == "N":
                self.cell.pollution = neighbor.pollution / 2 + self.cell.pollution
            if direction == "W" and neighbor.wind == "E":
                self.cell.pollution = neighbor.pollution / 2 + self.cell.pollution
            if direction == "E" and neighbor.wind == "W":
                self.cell.pollution = neighbor.pollution / 2 + self.cell.pollution

        # calculate temperature change
        self.cell.temperature = np.mean(
            [
                self.cell.temperature,
                self.cell.neighbors.mean_of()["temp_mean"] * (1 + factors["temp"]),
                self.cell.temperature * (1 + self.cell.pollution),
            ]
        )

        if self.cell.temperature > temp_range["max"]:
            self.cell.temperature = temp_range["max"]
        elif self.cell.temperature < temp_range["min"]:
            self.cell.temperature = temp_range["min"]


class Sea(State):
    state_symbol = "S"
    state_color = "#1273de"
    temp_range = {"min": 0, "max": 35}
    factors = {"temp": -0.2}

    def effect(self):
        self.calculate_weather_change(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["min"]:
            self.cell.transition_enqueue(self.cell.state_map["I"])  # change to Ice


class Ice(State):
    state_symbol = "I"
    state_color = "#ffffff"
    temp_range = {"min": -50, "max": 0}
    factors = {"temp": -0.4}

    def effect(self):
        self.calculate_weather_change(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["max"]:
            self.cell.transition_enqueue(self.cell.state_map["S"])  # change to Sea


class Forest(State):
    state_symbol = "F"
    state_color = "#7ed321"
    temp_range = {"min": 0, "max": 30}
    factors = {"temp": -0.1}

    def effect(self):
        self.calculate_weather_change(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["max"]:
            self.cell.transition_enqueue(self.cell.state_map["D"])  # change to Desert
        elif self.cell.temperature == self.temp_range["min"]:
            self.cell.transition_enqueue(self.cell.state_map["I"])  # change to Ice


class Desert(State):
    state_symbol = "D"
    state_color = "#f8e71c"
    temp_range = {"min": 30, "max": 50}
    factors = {"temp": 0.5}

    def effect(self):
        self.calculate_weather_change(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["min"]:
            self.cell.transition_enqueue(self.cell.state_map["F"])  # change to Forest


class City(State):
    state_symbol = "C"
    state_color = "#9b9b9b"
    temp_range = {"min": 0, "max": 40}
    factors = {"temp": 0.8}

    def effect(self):
        self.calculate_weather_change(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["max"]:
            self.cell.transition_enqueue(self.cell.state_map["D"])  # change to Desert

        self.cell.pollution = self.cell.pollution + 0.1


class Mountain(State):
    state_symbol = "M"
    state_color = "#57360e"
    temp_range = {"min": -20, "max": 20}
    factors = {"temp": -0.1}

    def effect(self):
        self.calculate_weather_change(self.temp_range, self.factors)
