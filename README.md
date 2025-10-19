# Over the Air Character Recognition

# AirChar IMU Data Acquisition and Augmentation

This repository contains the workflow used to **acquire**, **store**, and **augment** inertial data for the _AirChar_ project, focused on **handwritten character recognition in the air** using motion sensors.

---

## Overview

The system is based on an **Arduino Nano 33 BLE Sense**, which includes a built-in **9-axis IMU (LSM9DS1)** capable of measuring 3-axis acceleration and angular velocity.

Data collection, storage, and preprocessing are divided into three main components:

1. **`AirCharLogger.ino`** – Arduino firmware for real-time data acquisition.  
2. **`main.py`** – Python script to download serial data and save it into structured CSV files.  
3. **`dataAug.py` / `main.py`** – Python modules for data augmentation through 3D vector rotations.

---

## ⚙️ 1. Data Acquisition

The Arduino sketch [`AirCharLogger.ino`](./AirCharLogger.ino) configures the IMU and continuously logs:

- **Accelerometer:** `AccX`, `AccY`, `AccZ` (in *m/s²*)  
- **Gyroscope:** `GyrX`, `GyrY`, `GyrZ` (in *°/s*)  

Each record corresponds to a single IMU reading captured at **100 Hz**.  
Data is sent via the **serial port** to a host computer.

---

## 💾 2. Data Download and Storage

A Python script (e.g., [`download_data.py`](./download_data.py)) reads the serial output and saves it into a structured CSV file with the following format:


