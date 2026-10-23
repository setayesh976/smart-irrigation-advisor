# Irrigation Control Simulator

A rule-based simulation of a smart sprinkler control system for a farm, built in Python.

## Background

This project was inspired by watching a family member irrigate crops manually, deciding by hand which areas needed water and for how long. I wanted to explore how a program could make that same kind of decision automatically — and, since irrigation and fertilizing are closely related tasks on a real farm, I extended it to also track fertilizer needs.

## Features

- Simulates soil moisture readings for multiple sprinkler zones (standing in for real sensor data)
- Decides which zones need irrigation using a fixed moisture threshold
- Calculates irrigation duration based on how dry each zone is (drier zones get watered longer)
- Picks a flow rate ("Fast" or "Normal") depending on how severe the moisture deficit is
- Fertilizer tracking — each crop type has its own standard feeding interval; the system flags zones that are overdue and calculates how much fertilizer that crop needs
- Prints a full cycle summary: zones watered, total irrigation time, zones fertilized, total fertilizer used

## How It Works

This is a rule-based simulation, not a trained machine learning model. Every decision here — whether to irrigate, for how long, at what flow rate, and whether to fertilize — comes from direct comparisons against fixed thresholds and simple arithmetic, not from a model trained on data:

irrigate_if: moisture < threshold
duration = (threshold - moisture) / 10 × minutes_per_10_points
flow_rate = "Fast" if deficit >= 20 else "Normal"
fertilize_if: days_since_fertilized >= crop_specific_interval

I chose this approach because it's simple to build and explain with the tools I currently know. A more advanced version of this idea — using real soil sensors and weather data, with a model trained to predict moisture and nutrient needs ahead of time rather than just reacting to the current reading — is something I'd like to build as I learn more about AI and machine learning. This project is a first, simplified step toward that larger idea, not the finished version of it.

## How To Run

python irrigation_simulator.py

## Notes

Moisture and fertilizer timing are randomly simulated each run, since no real sensor hardware is connected in this version. The fertilizer intervals and amounts are simplified reference values I set myself, not measured agricultural data. The logic throughout is intentionally kept simple — comparisons and basic arithmetic — rather than using any ML library.
