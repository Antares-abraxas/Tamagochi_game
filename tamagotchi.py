import sys, pickle, datetime

from PyQt5 import QtCore, QtGui, QtWidgets, uic

ui = uic.loadUiType("tamagotchi.ui")[0]

class TamagotchiWindow(QtWidgets.QMainWindow, ui):
    """Класс для создания главного окна

    :param main_window: Главное окно программы
    :type main_window: class:'TamagotchiWindow'
    :param ui: Данные о пользовательском интерфейсе для создания главного окна
    """
    def __init__(self, parent = None):
        """Метод конструтора.
        Атрибуты:
        setupUI - инициализация пользовательского интерфейса.
        ambulance - факт нахождения питомца в больнице. Тип bool. Изначально False.
        walking - факт нахождения питомца на прогулке. Тип bool. Изначально False.
        sleeping - факт сна питомца. Тип bool. Изначально False.
        playing - факт игры питомцы. Тип bool. Изначально False.
        time_cycle - время дня в игре. Перезапускается, когда достигает 60. Тип int. 
        hunger - голод питомца. Изначально 0(сытый). Тип int.
        happiness - счастье питомца. Изначально 8(счастливый). Тип int.
        health - здоровье питомца. Изначально 8(здоровый). Тип int.
        forceAwakening - факт насильного пробуждения питомца. Тип bool. Изначально False.
        sleepImages - список изображений сна. Тип list.
        eatImages - список изображений кормления. Тип list.
        walkImages - список изображенйи прогулки. Тип list.
        playImages - список изображений игры. Тип list.
        ambulanceImages - список изображений больницы. Тип list.
        dinoImages - список стандартных изображений питомца. Тип list.
        imageList - список изображений, которые выводятся на экран. Изначально dinoImages. Тип list.
        imageIndex - индекс показываемого изображения. Тип int.
        timer1 - Обратный таймер, состоящий из 0,5 секунд. Для создания анимаций.
        timer2 - Обратный таймер, состоящий из 5 секунд. Так называемый 'tick'.
        :param parent: Родитель окна. В нашем случае отсутствует.
        :type parent: None
        """
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.ambulance = False
        self.walking = False
        self.sleeping = False
        self.playing = False
        self.eating = False
        self.time_cycle = 0
        self.hunger = 0
        self.happiness = 8
        self.health = 8
        self.forceAwakening = False
        self.sleepImages = ["sleep1.gif","sleep2.gif","sleep3.gif","sleep4.gif"]
        self.eatImages = ["eat1.gif", "eat2.gif"]
        self.walkImages = ["walk1.gif", "walk2.gif", "walk3.gif", "walk4.gif"]
        self.playImages = ["play1.gif", "play2.gif"]
        self.ambulanceImages = ["doc1.gif", "doc2.gif"]
        self.dinoImages = ["pet1.gif", "pet2.gif", "pet3.gif"]
        self.imageList = self.dinoImages
        self.imageIndex = 0
        
        self.actionStop.triggered.connect(self.stop_Click)
        self.actionFeed.triggered.connect(self.feed_Click)
        self.actionWalk.triggered.connect(self.walk_Click)
        self.actionPlay.triggered.connect(self.play_Click)
        self.actionAmbulance.triggered.connect(self.ambulance_Click)
        
        self.timer1 = QtCore.QTimer(self)
        self.timer1.start(500)
        self.timer1.timeout.connect(self.animation_timer)
        self.timer2 = QtCore.QTimer(self)
        self.timer2.start(5000)
        self.timer2.timeout.connect(self.tick_timer)
        
        filehandle = True
        try:
            file = open("savedata.pkl", "rb")
        except:
            filehandle = False
        if filehandle:
            save = pickle.load(file)
            file.close()
        else:
            save = [8, 8, 0, datetime.datetime.now(), 0]
            
        self.happiness = save[0]
        self.health = save[1]
        self.hunger = save[2]
        moment = save[3]
        self.time_cycle = save[4]

        difference = datetime.datetime.now() - moment
        ticks = int(difference.seconds / 50)
        for i in range(0, ticks):
            self.time_cycle += 1
            if self.time_cycle == 60:
                self.time_cycle = 0
            if self.time_cycle <= 48:
                self.sleeping = False
                if self.hunger < 8:
                    self.hunger += 1
            else:
                self.sleeping = True
                if self.hunger < 8 and self.time_cycle % 3 == 0:
                    self.hunger += 1
            if self.hunger == 7 and (self.time_cycle % 2 == 0) and self.health > 0:
                self.health -= 1
            if self.hunger == 8 and self.health > 0:
                self.health -=1
                
        if self.sleeping:
            self.imageList = self.sleepImages
        else:
            self.imageList = self.dinoImages
            
    def sleep_test(self):
        """Метод проверки сна питомца. Если питомец спит, то выводится предупреждение с выбором ответа.
        Меняет значения sleeping и forceAwakening, если игрок выбрал 'Да'.
        :return: True, если питомец не спит, False, если спит.
        :rtype: bool
        """
        if self.sleeping:
            result = (QtWidgets.QMessageBox.warning(self, "ВНИМАНИЕ", "Насильное пробуждение приведет к недовольству питомца. Уверены, что хотите его разбудить?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No))
            if result == QtWidgets.QMessageBox.Yes:
                self.sleeping = False
                self.happiness -= 4
                self.forceAwakening = True
                return True
            else:
                return False
        else:
            return True
        
    def ambulance_Click(self):
        """Функция, срабатывающая, если игрок нажимает на кпонку 'Больница'. Срабатывает, только если питомец не спит. Сменяет изображения на экране на изображения больницы.
        Присвает аттрибуту ambulance значение True,
        walking, eating, playing - False.
        """
        if self.sleep_test():
            self.imageList = self.ambulanceImages
            self.ambulance = True
            self.walking = False
            self.eating = False
            self.playing = False
            
    def feed_Click(self):
        """Функция, срабатывающая, если игрок нажимает на кпонку 'Кормить'. Срабатывает, только если питомец не спит. Сменяет изображения на экране на изображения кормления.
        Присвает аттрибуту eating значение True,
        walking, playing, ambulance - False.
        """
        if self.sleep_test():
            self.imageList = self.eatImages
            self.eating = True
            self.walking = False
            self.playing = False
            self.ambulance = False
            
    def play_Click(self):
        """Функция, срабатывающая, если игрок нажимает на кпонку 'Играть'. Срабатывает, только если питомец не спит. Сменяет изображения на экране на изображения игры.
        Присвает аттрибуту playing значение True,
        walking, eating, ambulance - False.
        """
        if self.sleep_test():
            self.imageList = self.playImages
            self.playing = True
            self.walking = False
            self.eating = False
            self.ambulance = False
            
    def walk_Click(self):
        """Функция, срабатывающая, если игрок нажимает на кпонку 'Выгуливать'. Срабатывает, только если питомец не спит. Сменяет изображения на экране на изображения выгуливания.
        Присвает аттрибуту walking значение True,
        eating, playing, ambulance - False.
        """
        if self.sleep_test():
            self.imageList = self.walkImages
            self.walking = True
            self.eating = False
            self.playing = False
            self.ambulance = False
            
    def stop_Click(self):
        """Функция, срабатывающая, если игрок нажимает на кпонку 'Стоп'. Срабатывает, только если питомец не спит. Сменяет изображения на экране на стандартные изображения.
        Присвает аттрибутам walking, eating, playing, ambulance значение False.
        """
        if not self.sleeping:
            self.imageList = self.dinoImages
            self.walking = False
            self.eating = False
            self.playing = False
            self.ambulance = False
            
    def animation_timer(self):
        """Функция, создающая анимацию сменой изображений. Шкалам Hunger, Happiness, Health устанавливает новые значения."""
        if self.sleeping and not self.forceAwakening:
            self.imageList = self.sleepImages
        self.imageIndex += 1
        if self.imageIndex >= len(self.imageList):
            self.imageIndex = 0
        icon = QtGui.QIcon()
        current_image = self.imageList[self.imageIndex]
        icon.addPixmap(QtGui.QPixmap(current_image), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.petPic.setIcon(icon)
        self.Hunger.setProperty("value", (8 - self.hunger) * (100 / 8.0))
        self.Happiness.setProperty("value", self.happiness * (100 / 8.0))
        self.Health.setProperty("value", self.health * (100 / 8.0))
        
    def tick_timer(self):
        """Функция, отвечающая за ход времени в игре и изменения параметров питомца с течением времени."""
        self.time_cycle += 1
        if self.time_cycle == 60:
            self.time_cycle = 0
        if self.time_cycle <= 48 or self.forceAwakening:
            self.sleeping = False
        else:
            self.sleeping = True
        if self.time_cycle == 0:
            self.forceAwakening = False
        if self.ambulance:
            self.health += 1
            self.hunger += 1
        elif self.walking:
            self.happiness += 1
            self.health += 1
            self.hunger += 1
        elif self.playing:
            self.happiness += 1
            self.hunger += 1
        elif self.eating:
            self.hunger -= 2
        elif self.sleeping:
            if self.time_cycle % 3 == 0:
                self.hunger += 1
        else:
            self.hunger += 1
            if self.time_cycle % 2 == 0:
                self.happiness -= 1
        if self.hunger > 8:
            self.hunger = 8
        if self.hunger < 0:
            self.hunger = 0
        if self.hunger == 7  :
            self.health -= 1
        if self.hunger == 8:
            self.health -=1
        if self.health > 8:
            self.health = 8
        if self.health < 0:
            self.health = 0
        if self.happiness > 8:
            self.happiness = 8
        if self.happiness < 0:
            self.happiness = 0
        self.Hunger.setProperty("value", (8 - self.hunger) * (100 / 8.0))
        self.Happiness.setProperty("value", self.happiness *(100 / 8.0))
        self.Health.setProperty("value", self.health * (100 / 8.0))

    def closeEvent(self, event):
        """Функция закрытия окна и сохранения перед закрытием."""
        file = open("savedata.pkl", "wb")
        save = [self.happiness, self.health, self.hunger, datetime.datetime.now(), self.time_cycle]
        pickle.dump(save, file)
        event.accept()
        
app = QtWidgets.QApplication(sys.argv)
myapp = TamagotchiWindow()
myapp.show()
app.exec_()
