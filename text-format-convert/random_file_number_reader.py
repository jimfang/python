__author__ = 'dwight'

# Write a function that writes a series of random numbers to a file. Each random number should be in the range of 1
# through 100. The application should let the user specify how many random numbers the file will hold. Write another
# function that will read the random numbers from the file, display the numbers, and then display the following data:
# (1) the total of the numbers, and (2) the number of random numbers read from the file.


import random


def main():
    name = 'random_number_file.txt'
    file_length = int(input('Enter amount of random numbers for file: '))
    create_random_number_file(name, file_length)
    count, total = read_random_number_file(name)
    print()
    print('Number of Lines: ' + str(count))
    print('Random Number Total: ' + str(total))


def create_random_number_file(filename, length):
    bottom_of_random_range = 1
    top_of_random_range = 100
    file = open(filename, 'w')
    for number in range(length):
        file.write(str(random.randint(bottom_of_random_range, top_of_random_range)) + '\n')
    file.close()


def read_random_number_file(filename):
    file = open(filename, 'r')
    line = file.readline()
    read_count = 0
    random_total = 0
    while line != '':
        print(line.rstrip('\n'))
        random_total += int(line.rstrip('\n'))
        read_count += 1
        line = file.readline()

    return read_count, random_total


main()
