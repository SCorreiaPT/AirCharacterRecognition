/** ==============================================================================
# AirChar - The in-the-Air Handwritten Dataset for
# Character Recognition Based on Acceleration (IMU) Data
# ==============================================================================
# Laboratory of Electronics and Instrumentation (LEI)
# Portalegre Polytechnic University
# T. M. D. Correia, S. D. Correia, and J. P. Matos-Carvalho
# ==============================================================================
# Copyright 2024 LEI. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
# ==============================================================================
*/

/** 
@brief This program collects IMU data from a LSM9DS1 IMU sensor and stores it in the RAM.
The user can download the data through the serial port.
*/
#include <Arduino_LSM9DS1.h>

#define SAMPLE_RATE 100                         // Sampling rate in Hz
#define DURATION 30                             // Storage duration in seconds
#define BUFFER_SIZE SAMPLE_RATE * DURATION      // Buffer size based on the maximum duration allowed

float accelX[BUFFER_SIZE];                      // Buffers to store the data
float accelY[BUFFER_SIZE];
float accelZ[BUFFER_SIZE];
float gyroX[BUFFER_SIZE];
float gyroY[BUFFER_SIZE];
float gyroZ[BUFFER_SIZE];

volatile bool sampling = false;                 // State Variable
volatile int sampleIndex = 0;                   // Index for saving data

/**
 * @brief Setup function to initialize serial communication and IMU sensor.
 */
void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  sampling = false;

  Serial.println("Enter 'S' to Start/Stop sampling, 'D' to Download and 'X' to Exit program.");
}

/**
 * @brief Start sampling data from the IMU sensor.
 */
void startSampling() {
  sampling = true;
  sampleIndex = 0;
  Serial.println("Starting sampling... Press Enter to stop.");
}

/**
 * @brief Stop sampling data from the IMU sensor.
 */
void stopSampling() {
    sampling = false;
    Serial.println("Stopping sampling...");
}

/**
 * @brief Download the sampled data via serial communication.
 */
void downloadData() {
  for (int i = 0; i < sampleIndex; i++) {
    Serial.print(accelX[i], 6);
    Serial.print(";");
    Serial.print(accelY[i], 6);
    Serial.print(";");
    Serial.print(accelZ[i], 6);
    Serial.print(";");
    Serial.print(gyroX[i], 6);
    Serial.print(";");
    Serial.print(gyroY[i], 6);
    Serial.print(";");
    Serial.println(gyroZ[i], 6);
  }
}

/**
 * @brief Main loop function to handle commands and perform sampling.
 */
void loop() {
  // Reads and processes incoming data
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (!sampling) {
      if (command.equalsIgnoreCase("S")) {
        startSampling();
      } else if (command.equalsIgnoreCase("D")) {
        downloadData();
      } else if (command.equalsIgnoreCase("X")) {
        stopSampling();
      }
    } else {
      if (command.equals("")) { // Pressing Enter without any command
        stopSampling();
      } else {
        Serial.println("Invalid command. Press Enter to stop.");
      }
    }
  }

  // Data Acquisition  
  if (sampling && sampleIndex < BUFFER_SIZE) {
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      float ax, ay, az;
      float gx, gy, gz;

      IMU.readAcceleration(ax, ay, az);
      IMU.readGyroscope(gx, gy, gz);

      accelX[sampleIndex] = ax;
      accelY[sampleIndex] = ay;
      accelZ[sampleIndex] = az;
      gyroX[sampleIndex] = gx;
      gyroY[sampleIndex] = gy;
      gyroZ[sampleIndex] = gz;

      sampleIndex++;

      delay(1000 / SAMPLE_RATE);
    } else {
      Serial.println("Sample failed");
      Serial.println(sampleIndex);
    }
  }
}
