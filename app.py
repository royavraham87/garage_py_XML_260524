from enum import Enum
import os
import xml.etree.ElementTree as ET
from icecream import ic

garage = []

class Actions(Enum):
    ADD = 1
    DELETE = 2
    PRINT = 3
    UPDATE = 4
    EXIT = 5 
    COUNT_CARS = 6
    NULIFY_CARS_ARRAY = 7

def menu():
    ic("Displaying menu options:")  # Using ic for output
    # Display all available actions
    for action in Actions:
        ic(f'{action.value} - {action.name}')
    # Return the selected action as an enum member
    return Actions(int(input("Please select an action: ")))

def add_car():
    brand = input("What brand? ")
    model = int(input("What model? "))
    color = input("What color? ")

    car_element = ET.Element("car")
    brand_element = ET.SubElement(car_element, "brand")
    brand_element.text = brand
    model_element = ET.SubElement(car_element, "model")
    model_element.text = str(model)
    color_element = ET.SubElement(car_element, "color")
    color_element.text = color

    garage.append(car_element)

def print_cars():
    if not garage:
        ic("The garage is empty.")
    for index, car in enumerate(garage):
        brand = car.find("brand").text
        model = car.find("model").text
        color = car.find("color").text
        ic(f"({index}) brand: {brand}, model: {model}, color: {color}")

def del_car():
    print_cars()
    car_number = int(input("Please select a car number: "))
    if 0 <= car_number < len(garage):
        ic(f'{ET.tostring(garage[car_number], encoding="unicode")} was deleted')
        garage.pop(car_number)
    else:
        ic("Invalid car number.")

def upd_car():
    print_cars()
    car_number = int(input("Please select a car number to update: "))
    if 0 <= car_number < len(garage):
        brand = input("New brand? ")
        model = int(input("New model? "))
        color = input("New color? ")
        
        car = garage[car_number]
        car.find("brand").text = brand
        car.find("model").text = str(model)
        car.find("color").text = color
        
        ic("Car updated successfully.")
    else:
        ic("Invalid car number.")

def load_garage_from_xml(filename):
    if not os.path.exists(filename):
        ic("File not found:", filename)
        return []  # Return an empty list if the file does not exist

    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        ic("Loaded data:", root)
        return list(root)
    except ET.ParseError:
        ic("XML parsing error:", filename)
        return []  # Return an empty list if the file is empty or contains invalid XML

def save_garage_to_xml(garage, filename):
    root = ET.Element("garage")
    for car in garage:
        root.append(car)

    tree = ET.ElementTree(root)
    tree.write(filename)

def count_cars():
    ic(f"There are {len(garage)} cars in the garage.")

def nulify_cars_array():
    confirmation = input("Are you sure you want to delete all the cars from the garage? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        garage.clear()
        ic("All cars have been deleted from the garage.")
    else:
        ic("Operation cancelled. No cars were deleted.")

if __name__ == "__main__":
    ic("Loading garage data...")  # Using ic for output
    garage = load_garage_from_xml('garage.xml')

    while True:
        user_selection = menu()
        ic(f"User selected action: {user_selection}")
        if user_selection == Actions.EXIT:
            save_garage_to_xml(garage, 'garage.xml')
            exit()
        elif user_selection == Actions.ADD:
            add_car()
        elif user_selection == Actions.PRINT:
            print_cars()
        elif user_selection == Actions.DELETE:
            del_car()
        elif user_selection == Actions.UPDATE:
            upd_car()
        elif user_selection == Actions.COUNT_CARS:
            count_cars()
        elif user_selection == Actions.NULIFY_CARS_ARRAY:
            nulify_cars_array()
