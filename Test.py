from collections import Counter
import random
import psycopg2
import numpy as np


Bincom_staffs_colour =  {
    "MONDAY": ["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK", "BLUE", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"],
    "TUESDAY": ["ARSH", "BROWN", "GREEN", "BROWN", "BLUE", "BLUE", "BLEW", "PINK", "PINK", "ORANGE", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "WHITE", "BLUE", "BLUE", "BLUE"],
    "WEDNESDAY": ["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK", "RED", "YELLOW", "ORANGE", "RED", "ORANGE", "RED", "BLUE", "BLUE", "WHITE", "BLUE", "BLUE", "WHITE", "WHITE"],
    "THURSDAY": ["BLUE", "BLUE", "GREEN", "WHITE", "BLUE", "BROWN", "PINK", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"],
    "FRIDAY": ["GREEN", "WHITE", "GREEN", "BROWN", "BLUE", "BLUE", "BLACK", "WHITE", "ORANGE", "RED", "RED", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "WHITE"]
}


# # #WHICH COLOR OF SHIRT IS THE MEAN COLOR?
daily_modes = {day: Counter(colors).most_common(1)[0][0] for day, colors in Bincom_staffs_colour.items()}

# Calculate overall mode
overall_mode = Counter(daily_modes.values()).most_common(1)[0][0]

print("Mean colour : ", overall_mode)





# QUESTION (2) WHICH COLOUR IS MOSTLY WORN THROUGTHOUT THE WEEK?

#USING COUNTER TO Count the frequency occurance of the colours
Staffs_colour =  Counter(colour for day in Bincom_staffs_colour.values() for colour in day)

common_colour = Staffs_colour.most_common(1)[0][0]
print(common_colour)  


# QUESTION (3) WHiCH COLOURS IS THE MEDIAN?
for day, colours in Bincom_staffs_colour.items():
    colour_counts = Counter(colours)
    sortedcolours = sorted(colour_counts.keys())
    total_count = sum(colour_counts.values())
    cumulative_count = 0
    median_color = None
    

    for color in sortedcolours:
        cumulative_count += colour_counts[color]
        if cumulative_count >= total_count / 2:
            median_color = color
            break
    
    print(f"color for {day}: {median_color}")


# QUESTION (4) Get the variance of the colors


def calculate_variance(colors):
    unique_colors, counts = np.unique(colors, return_counts=True)
    total_count = len(colors)
    probabilities = counts / total_count
    variance = np.sum(probabilities * (1 - probabilities))
    return variance

variances = {}
for day, colors in Bincom_staffs_colour.items():
    variances[day] = calculate_variance(colors)

# Print variances
for day, variance in variances.items():
    print(f"Variance for {day}: {variance:.4f}")




# QUESTION (8) Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
binary_number = random.randint(0, 15) 

# Convert binary number to base 10
decimal_number = int(bin(binary_number)[2:])  

print("Generated Binary Number:", format(binary_number, '04b'))  
print("Converted to Base 10:", decimal_number)




# QUESTION (9) Write a program to sum the first 50 fibonacci sequence.
def fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

# Calculate Fibonacci sequence
fib_sequence = fibonacci(50)

# Sum the Fibonacci sequence
fib_sum = sum(fib_sequence)

print("The sum of the first 50 Fibonacci numbers is:", fib_sum)


# CONNECTING TO MY LOCAL_POSTGRESQL DATABASE
try:
    connection = psycopg2.connect(
        dbname="Test",
        user="postgres",
        password="Django@2024",
        host="localhost",
        port= 8000  
    )
    print("Connected to database successfully")
    
    cursor = connection.cursor()


    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staffs_colour (
            day VARCHAR(20),
            colour VARCHAR(20)
        )
    """)

    # Insert data into the table
    for day, colours in Bincom_staffs_colour.items():
        for colour in colours:
            cursor.execute("INSERT INTO staffs_colour (day, colour) VALUES (%s, %s)", (day, colour))

    # Commit the transaction
    connection.commit()
    print("Data inserted successfully")

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Close cursor and connection
    cursor.close()
    connection.close()