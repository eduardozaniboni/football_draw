import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
import json
import random
import numpy as np


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.names = []
        self.attacks = []
        self.defenses = []

        self.name_edit = QLineEdit()
        self.attack_edit = QLineEdit()
        self.attack_edit.setValidator(QIntValidator(1, 10, self))
        self.defense_edit = QLineEdit()
        self.defense_edit.setValidator(QIntValidator(1, 10, self))

        name_validator = QRegExpValidator(QRegExp("[a-zA-Z]+"), self)
        self.name_edit.setValidator(name_validator)

        self.add_button = QPushButton('Adicionar')
        self.add_button.clicked.connect(self.addPerson)

        self.team_size_edit = QLineEdit()
        self.team_size_edit.setValidator(QIntValidator(1, 100, self))
        self.team_size_edit.setPlaceholderText('Número de pessoas por time')

        self.sort_button = QPushButton('Sortear')
        self.sort_button.clicked.connect(self.sortTeams)

        self.output = QTextEdit()

        self.save_button = QPushButton('Salvar Lista')
        self.save_button.clicked.connect(self.saveList)

        self.import_button = QPushButton('Importar Lista')
        self.import_button.clicked.connect(self.importList)

        self.people_list = QTextEdit()
        self.people_list.setReadOnly(True)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('Nome:'))
        hbox1.addWidget(self.name_edit)
        hbox1.addWidget(QLabel('Ataque:'))
        hbox1.addWidget(self.attack_edit)
        hbox1.addWidget(QLabel('Defesa:'))
        hbox1.addWidget(self.defense_edit)
        hbox1.addWidget(self.add_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.team_size_edit)
        hbox2.addWidget(self.sort_button)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.import_button)
        hbox3.addWidget(self.save_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.people_list)
        vbox.addWidget(self.output)

        self.setLayout(vbox)

        self.setWindowTitle('Sorteador de Times')
        self.show()

    def addPerson(self):
        name = self.name_edit.text()
        attack = int(self.attack_edit.text())
        defense = int(self.defense_edit.text())

        self.names.append(name)
        self.attacks.append(attack)
        self.defenses.append(defense)

        self.name_edit.clear()
        self.attack_edit.clear()
        self.defense_edit.clear()

        self.updatePeopleList()

    def sortTeams(self):
        team_size = int(self.team_size_edit.text())

        num_players = len(self.names)
        num_teams = num_players // team_size

        # Criar uma lista de jogadores com sua pontuação total
        players = [(name, attack + defense) for name, attack,
                   defense in zip(self.names, self.attacks, self.defenses)]

        # Criar uma lista de times vazios
        teams = [[] for _ in range(num_teams)]

        # Iterar até que todos os jogadores sejam distribuídos
        while players:
            # Iterar sobre os times disponíveis
            for i, team in enumerate(teams):
                # Verificar se a lista de jogadores está vazia
                if not players:
                    break
                # Calcular a soma total de habilidades do time atual
                team_score = sum(score for _, score in team)
                # Encontrar o jogador que minimiza a diferença total de habilidades entre os times
                min_diff_player_index = min(range(len(players)), key=lambda j: abs(
                    team_score + players[j][1] - sum(sum(score for _, score in t) for t in teams)))
                # Adicionar jogador ao time atual
                teams[i].append(players.pop(min_diff_player_index))

        # Exibir a formação dos times
        self.output.clear()
        total_team_scores = []  # Lista para armazenar os valores totais de cada time
        for i, team in enumerate(teams):
            # Calcular o valor total do time
            team_score = sum(score for _, score in team)
            # Adicionar o valor total do time à lista
            total_team_scores.append(team_score)
            self.output.append(f'Time {i+1}: {team_score} pontos')
            for player in team:
                self.output.append(f'  Nome: {player[0]}, Ataque: {self.attacks[self.names.index(
                    player[0])]}, Defesa: {self.defenses[self.names.index(player[0])]}')

    def saveList(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Salvar Lista de Pessoas", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                for i in range(len(self.names)):
                    f.write(f"{self.names[i]}, {self.attacks[i]}, {
                            self.defenses[i]}\n")

    def importList(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Importar Lista de Pessoas", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                data = json.load(f)
                people_data = data.get('people', [])
                self.names.clear()
                self.attacks.clear()
                self.defenses.clear()
                for person in people_data:
                    self.names.append(person.get('name', ''))
                    self.attacks.append(person.get('attack', 0))
                    self.defenses.append(person.get('defense', 0))
        self.updatePeopleList()

    def updatePeopleList(self):
        self.people_list.clear()
        for i in range(len(self.names)):
            self.people_list.append(f'Nome: {self.names[i]}, Ataque: {
                                    self.attacks[i]}, Defesa: {self.defenses[i]}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
