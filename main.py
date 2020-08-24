import deliveryalgorithm

deliveryalgorithm.load_tables()

deliveryalgorithm.run_delivery_algorithm()

# Display user interface
user_input = "5:00 PM"

while (user_input != "exit"):
    #user_input = input("Enter a time in the format HH:MM to see the status of packages or type 'exit' to stop: ")

    print("{:<4} {:<40} {:<20} {:<8} {:<8} {:<8} {}".format("ID", "Address", "City","State","Zip","Mass","Status"))

    package_status_list = deliveryalgorithm.get_status_list(user_input)

    for i in range(0, 39, 1):
        print("{:<4} {:<40} {:<20} {:<8} {:<8} {:<8} {}".format(package_status_list[i][0], package_status_list[i][1],
                                                             package_status_list[i][2], package_status_list[i][3],
                                                             package_status_list[i][4], package_status_list[i][5],
                                                             package_status_list[i][6]))

    user_input = "exit"
