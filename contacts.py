contacts = {
    "Number":4,
    "Students":
    [
        {"name":"Andy", "email":"andy@myezbrew"},
        {"name":"Jeff", "email":"jeff@amazon.com"},
        {"name":"Lisa", "email":"lisa@myezbrew"},
        {"name":"Parker", "email":"parker@myezbrew"}
    ]
}

for student in contacts["Students"]:
    print(student)

for student in contacts["Students"]:
    print(student["email"])