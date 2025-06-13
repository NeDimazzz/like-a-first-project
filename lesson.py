#Создай класс Task, который позволяет управлять задачами (делами).
#У задачи должны быть атрибуты: описание задачи, срок выполнения
#и статус (выполнено/не выполнено). Реализуй функцию для добавления задач,
#отметки выполненных задач и вывода списка текущих (не выполненных) задач.

class Task ():
    def __init__(self):
        self.tasks = []

    def add(self, time, description):

        self.tasks.append({'time': time, 'description' : description,
                           'status' : 'не выполнено'})


    def complite(self, description ):
        for task in self.tasks:
            if task['description']  == description:
                task['status'] = 'выполнено'
                print(f'задача {description} : выполнено')
            else:
                print(f'задача {description} : не найдена')

    def info(self):
        print(f'текущие задачи')
        for task in self.tasks:
            if task['status']  == 'не выполнено':
                print(f' {task['description']} - {task['time']}')

t = Task()
t.add('01.07.2025','Купить книгу')
t.add('10.07.2025','Прочитать Книгу')
t.add('21.07.2025','Использовать книгу')

t.info()

t.complite('Купить книгу')

t.info()
