import random


class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_hw(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
                course in lecturer.courses_attached and
                course in self.courses_in_progress):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __avarage_grade(self):
        total = 0
        counter = 0
        for course, grades in self.grades.items():
            total += sum(grades)
            counter += len(grades)
        return total / counter

    def __str__(self):
        res = (f'Имя: {self.name}\nФамилия: {self.surname}\n'
               f'Средняя оценка за домашние задания: '
               f'{self.__avarage_grade():.1f}\n'
               f'Курсы в процессе изучения: '
               f'{", ".join(self.courses_in_progress)}\n'
               f'Завершенные курсы: {", ".join(self.finished_courses)}')
        return res

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Not a Student!')
            return
        return self.__avarage_grade() < other.__avarage_grade()


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __avarage_grade(self):
        total = 0
        counter = 0
        for course, grades in self.grades.items():
            total += sum(grades)
            counter += len(grades)
        return total / counter

    def __str__(self):
        res = (f'Имя: {self.name}\nФамилия: {self.surname}\n'
               f'Средняя оценка за лекции: {self.__avarage_grade():.1f}')
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a Lecturer!')
            return
        return self.__avarage_grade() < other.__avarage_grade()


class Reviewer(Mentor):

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res


def avarage_grate_on_course(students, course):
    total = 0
    counter = 0
    for i in range(len(students)):
        for key, grades in students[i].grades.items():
            if key == course:
                total += sum(grades)
                counter += len(grades)
    return total / counter


def avarage_grate_of_lectors(lectors, course):
    total = 0
    counter = 0
    for i in range(len(lectors)):
        for key, grades in lectors[i].grades.items():
            if key == course:
                total += sum(grades)
                counter += len(grades)
    return total / counter


students = [Student('Иван', 'Иванов', 'м'),
            Student('Пётр', 'Петров', 'м'),
            Student('Фёдор', 'Фёдоров', 'м'),
            Student('Анна', 'Павлова', 'ж'),
            Student('Зоя', 'Зайцева', 'ж')]

for i in [0, 1, 3]:
    students[i].courses_in_progress += ['Python']
for i in [2, 4]:
    students[i].courses_in_progress += ['Java']

students[4].add_courses('Python')
students[2].add_courses('Курсы кройки и шитья')
students[1].add_courses('Русский язык (по правилам и без)')
students[1].add_courses('ТРИЗ')

lectors = [Lecturer('Василий', 'Тёркин'), Lecturer('Макар', 'Макаров')]
lectors[0].courses_attached += ['Python', 'C#']
lectors[1].courses_attached += ['Python', 'Java']

reviewer_1 = Reviewer('Дмитрий', 'Жук')
reviewer_1.courses_attached += ['Java', 'C#']
reviewer_2 = Reviewer('Владимир', 'Маничев')
reviewer_2.courses_attached += ['Python']

lesson = 0
while lesson < 10:
    for i in [0, 1, 3]:
        reviewer_2.rate_hw(students[i], 'Python', random.randint(1, 10))
    for i in [2, 4]:
        reviewer_1.rate_hw(students[i], 'Java', random.randint(1, 10))
    for i in [0, 1, 3]:
        students[i].rate_hw(lectors[0], 'Python', random.randint(1, 10))
        students[i].rate_hw(lectors[1], 'Python', random.randint(1, 10))
    for i in [2, 4]:
        students[i].rate_hw(lectors[1], 'Java', random.randint(1, 10))
    lesson += 1

print('\n\033[4;36mЭксперты, проверяющие домашние задания\033[0;0m')
print(reviewer_1)
print()
print(reviewer_2)
print('\n\033[4;36mЛекторы\033[0;0m')
for i in range(len(lectors)):
    print(lectors[i])
    #print(lectors[i].grades)
    print()
lectors.sort()
best = len(lectors) - 1
print((f'\033[3;32mЛучший лектор: '
       f'{lectors[best].surname + " " + lectors[best].name}\033[0;0m'))

print('\n\033[4;36mСтуденты в порядке возрастания среднего балла\033[0;0m')
students.sort()
for i in range(len(students)):
    print(students[i])
    #print(students[i].grades)
    print()

course_name = 'Python'
print((f'\033[3;35mСредняя оценка за домашние задания всех студентов курса '
       f'{course_name}: '
       f'{avarage_grate_on_course(students, course_name):.1f}'))

course_name = 'Java'
print((f'Средняя оценка за домашние задания всех студентов курса '
       f'{course_name}: '
       f'{avarage_grate_on_course(students, course_name):.1f}'))

print()
course_name = 'Python'
print((f'\033[3;34mСредняя оценка за лекции всех лекторов в рамках курса '
       f'{course_name}: '
       f'{avarage_grate_of_lectors(lectors, course_name):.1f}'))

course_name = 'Java'
print((f'Средняя оценка за лекции всех лекторов в рамках курса '
       f'{course_name}: '
       f'{avarage_grate_of_lectors(lectors, course_name):.1f}'))