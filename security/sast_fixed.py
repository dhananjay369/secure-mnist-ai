def run_demo(user_value):
    if not isinstance(user_value, str):
        raise TypeError("Input must be a string")

    print(user_value)
