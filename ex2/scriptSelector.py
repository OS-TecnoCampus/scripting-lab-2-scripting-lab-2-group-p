import task1
import task2
import task3
import task4
import task5
import task6

while True:
    mode = input(
        "Which script would you like to run (task1.py, task2.py, task3.py, task4.py, task5.py or task6.py)? "
        "(Or type EXIT to quit)").lower()  # Case insensitive
    if mode == "exit":
        break  # we exit the infinite loop
    elif mode == "task1.py":
        task1.main()
    elif mode == "task2.py":
        task2.main()
    elif mode == "task3.py":
        task3.main()
    elif mode == "task4.py":
        task4.main()
    elif mode == "task5.py":
        task5.main()
    elif mode == "task6.py":
        task6.main()
    else:
        print("Incorrect script name.")
