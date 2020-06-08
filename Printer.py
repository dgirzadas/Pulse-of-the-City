def loading_bar(percentage):
    if percentage < 100:
        print("[" + "-" * percentage + " " * (100 - percentage) + "] " + str(percentage) + "%", end='\r')
    else:
        print("[" + "-" * percentage + " " * (100 - percentage) + "] " + "Done!")