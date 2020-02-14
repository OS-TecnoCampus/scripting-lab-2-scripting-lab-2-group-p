import task1
import task2

while True:
    mode = input(
        "Which script would you like to run (task1.py, task2.py)? "
        "(Or type EXIT to quit)").lower()  # Case insensitive
    if mode == "exit":
        break  # we exit the infinite loop
    elif mode == "task1.py":
        task1.main()
    elif mode == "task2.py":
        task2.main()
    else:
        print("Incorrect script name.")
