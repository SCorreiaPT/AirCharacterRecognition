# ==============================================================================
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
"""
@brief This program collects IMU data from a serial port and saves it in text format.
The user can specify the character, subject identifier, version number, and sample number to generate filenames.
"""
import serial
import sys
import os


def process_response(response):
    """
    @brief Process the response from the serial input.

    @param response The response string from the serial input.
    @return A processed string with semicolon separated values or the original response if there's a ValueError.
    """
    try:
        values = response.split(';')
        return ";".join(values)
    except ValueError:
        return response


def get_user_input(prompt, validation_func, error_message):
    """
    @brief Get validated input from the user.

    @param prompt The input prompt for the user.
    @param validation_func The function to validate the input.
    @param error_message The error message to display on invalid input.
    @return The validated user input.
    """
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        else:
            print(error_message)


def generate_filename(character, subject, version_number, sample_number):
    """
    @brief Generate a filename based on character, subject, version number, and sample number.

    @param character The character being sampled.
    @param subject The subject identifier.
    @param version_number The version number of the sample.
    @param sample_number The sample number.
    @return The generated filename.
    """
    return f"{character}_s{subject}v{version_number}n{sample_number}p0a0f0.csv"
    # Symbol meaning
    # ...
    # p0 - No filter
    # a0 - With no augmented data
    # f0 - No added features


def write_header(file_path, filename, character, subject, version_number, sample_number):
    """
    @brief Write the header to the file.

    @param file_path The path to the file.
    @param filename The name of the file.
    @param character The character to be recognized.
    @param subject The subject associated with the dataset.
    @param version_number The version of the dataset.
    @param sample_number The sample number in the dataset.
    """
    header = f"""AirChar - The in-the-Air Handwritten Dataset
for Character Recognition Based on Acceleration (IMU) Data
#
IMU: LSM9DS1
Sampling Frequency: 100Hz
Size: ???
FileName: {filename}
Character: {character}
Subject: {subject}
Version: {version_number}
Sample Number: {sample_number}
Preprocessing Filter: No
Augmentation: No
Features: No
Format: csv
#
Label;accX;accY;accZ;gyrX;gyrY;gyrZ
"""
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        file.write(header)


def main():
    """
    @brief The main function to run the program. It initializes the serial connection, gets user inputs,
    handles data recording, and writes data to files.
    """
    port = 'COM4'
    baud_rate = 115200
    file_directory = 'C:\\Users\\scorr\\Clouds\Dropbox\\05 -IDT Management\\500 - IDT\\000 - DataSet\\Software\\S1_pyLogger_v1\\Samples\\A_rawData'

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f'Connected to port {port} with baud rate {baud_rate}')

        valid_words = ['IDLE', 'enter', 'backspace']

        character = get_user_input(
            'Enter the Character designed in-the-Air: ',
            lambda x: len(x) == 1 or x in valid_words,
            'Invalid input. Please enter a single character or a valid word (e.g., enter).'
        )

        # Initialize ascii_value with a default value
        ascii_value = None

        if character in valid_words:
            if character == 'IDLE':
                # Synchronous Idle
                ascii_value = 22
            if character == 'enter':
                # Carriage Return
                ascii_value = 13
            if character == 'backspace':
                # Backspace
                ascii_value = 8
        else:
            ascii_value = ord(character)

        subject = get_user_input(
            'Enter the subject ID: ',
            lambda x: x.isdigit() and len(x) <= 2,
            'Invalid subject ID. Please enter a valid number with up to 2 digits.'
        )

        subject = f"{int(subject):02}"

        version_number = get_user_input(
            'Enter the version number: ',
            lambda x: x.isdigit() and len(x) <= 2,
            'Invalid version number. Please enter a valid number with up to 2 digits.'
        )
        version_number = f"{int(version_number):02}"

        sample_number = get_user_input(
            'Enter the sample number: ',
            lambda x: x.isdigit(),
            'Invalid sample number. Please enter a valid number.'
        )
        sample_number = f"{int(sample_number):04}"

        filename = generate_filename(character, subject, version_number, sample_number)
        full_file_path = os.path.join(file_directory, filename)

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        write_header(full_file_path, filename, character, subject, version_number, sample_number)
        print(f'The file will be saved as: {full_file_path}')

        record_data = False

        while True:
            command = input(
                'Enter a command to send via serial port ("S" Start/stop, "D" - Download, or "X" to Exit): '
            )

            command_with_newline = command + '\n'

            ser.write(command_with_newline.encode())

            if command.upper() == 'X':
                print('Exiting the program.')
                break

            if command.upper() == 'D':
                record_data = True
                print('Starting to record data to the file.')

            while True:
                response = ser.readline().decode().strip()
                if response:
                    print(f'Received: {response}')
                    # processed_values = process_response(response)
                    processed_values = response
                    if record_data:
                        with open(full_file_path, mode='a', encoding='utf-8-sig') as file:
                            file.write(str(ascii_value) + ';' + processed_values + '\n')
                else:
                    if record_data:
                        record_data = False
                        sample_number = f"{int(sample_number) + 1:04}"
                        filename = generate_filename(character, subject, version_number, sample_number)
                        full_file_path = os.path.join(file_directory, filename)
                        write_header(full_file_path, filename, character, subject, version_number, sample_number)
                        print(f'The next file will be saved at: {full_file_path}')
                    break

        ser.close()

    except serial.SerialException as e:
        print(f'Error opening the serial port: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
