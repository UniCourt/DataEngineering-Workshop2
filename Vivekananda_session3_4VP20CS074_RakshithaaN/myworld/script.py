import random
# Simple function to print messages 
def print_msg():
    for i in range(10):
        print("Program completed")

# Generate random data
def generate():
    data = [random.randint(0, 99) for p in range(0, 1000)]
    return data

# Function to search 
def search_function(data):
    for i in data:
        if i in [100,200,300,400,500]:
            print("success")

def main():
    data=generate()
    search_function(data)
    print_msg()

main()
import random
from memory_profiler import profile
# Simple function to print messages 
@profile
def print_msg():
    for i in range(10):
        print("Program completed")

# Generate random data
@profile
def generate():
    data = [random.randint(0, 99) for p in range(0, 1000)]
    return data

# Function to search 
@profile
def search_function(data):
    for i in data:
        if i in [100,200,300,400,500]:
            print("success")

def main():
    data=generate()
    search_function(data)
    print_msg()

main()
