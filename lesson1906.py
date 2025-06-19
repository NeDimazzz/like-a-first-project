class Animal():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        pass

    def eat(self):
        print (f'{self.name} кушает')

class Bird(Animal):
    def make_sound(self):
        print('Кар Кар')

class Mammal(Animal):
    def make_sound(self):
        print('Гав')

class Reptaile(Animal):
    def make_sound(self):
        print('Щиииии')

def animal_sound(animals):
    for animal in animals:
        animal.make_sound()

class Zoo():
    def __init__(self):
        self.animals = []
        self.workers = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f'Животное {animal.name} добавлено в вольер')

    def add_worker(self, worker):
        self.workers.append(worker)
        print(f'Работник {worker} добавлено в зоопарк')

class ZooKeeper():
    def feed_animal(self,animal):
        print(f'Работник покормил {animal.name} ')

class Vet():
    def healf_animal(self,animal):
        print(f'Ветеринар подлечил {animal.name} ')

bird1 = Bird('Ворона', 1)
mammal1 = Mammal('Пес', 4)
reptaile1 = Reptaile('Хамелион', 2)

zoo = Zoo()
keeper = ZooKeeper()
vet = Vet()

zoo.add_animal(bird1)
zoo.add_animal(mammal1)
zoo.add_animal(reptaile1)


zoo.add_worker(keeper)
zoo.add_worker(vet)

animal_sound(zoo.animals)


keeper.feed_animal(mammal1)
vet.healf_animal(reptaile1)