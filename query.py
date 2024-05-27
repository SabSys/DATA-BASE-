import sys
import psycopg2
from PyQt5 import (QtGui, QtCore, QtWidgets)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(800, 800)
	
        
        main = QtWidgets.QWidget()
        self.setCentralWidget(main)
        main.setLayout(QtWidgets.QVBoxLayout())
        main.setFocusPolicy(QtCore.Qt.StrongFocus)

        
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)
		
        controls_panel = QtWidgets.QHBoxLayout()
        main.layout().addLayout(controls_panel)
        main.layout().addWidget(self.tableWidget)

        
        _label = QtWidgets.QLabel('From: ', self)
        _label.setFixedSize(50,20)
        self.from_box = QtWidgets.QComboBox() 
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)

        
        _label = QtWidgets.QLabel('  To: ', self)
        _label.setFixedSize(40,20)
        self.to_box = QtWidgets.QComboBox() 
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)

         
        _label = QtWidgets.QLabel('Hops: ', self)
        _label.setFixedSize(40,20)
        self.hop_box = QtWidgets.QComboBox() 
        self.hop_box.addItems( ['1', '2', '3'] )
        self.hop_box.setCurrentIndex( 2 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.hop_box)

        
        self.go_button = QtWidgets.QPushButton("Go!")
        self.go_button.clicked.connect(self.button_Go)
        controls_panel.addWidget(self.go_button)

        self.distance_button = QtWidgets.QPushButton("Distance")
        self.distance_button.clicked.connect(self.button_Distance)
        controls_panel.addWidget(self.distance_button)
           
        self.duration_button = QtWidgets.QPushButton("Durations")
        self.duration_button.clicked.connect(self.button_Duration)
        controls_panel.addWidget(self.duration_button)


        self.connect_DB()
                   
        self.show()
        

    def connect_DB(self):
        self.conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT distinct(name) FROM network_nodes_belfast ORDER BY name""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        for row in rows : 
            self.from_box.addItem(str(row[0]))
            self.to_box.addItem(str(row[0]))


    def button_Go(self):
        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = int(self.hop_box.currentText())

        rows = []

       # self.cursor.execute(""f"SELECT teacher.*, teaches.* FROM teaches, teacher WHERE teacher.id = teaches.id AND (teacher.name = '{_fromstation}' or teacher.name = '{_tostation}') """)
       # self.conn.commit()
       # rows += self.cursor.fetchall()

        if _hops == 1:
            self.cursor.execute(f"""
    select distinct A.name, C.route_name, B.name from network_nodes_belfast as A, network_nodes_belfast as B, routes_belfast as C, routes_bus_belfast as D, routes_bus_belfast as E WHERE A.stop_i=D.stop_i AND B.stop_i=E.stop_i and D.route_i=E.route_i AND C.route_i=D.route_i AND A.name='{_fromstation}' AND B.name='{_tostation}';
""")

            self.conn.commit()
            rows += self.cursor.fetchall()

        if _hops == 2 : 
            self.cursor.execute(f"""
    SELECT DISTINCT
        A.name AS depart,
        C.route_name AS premier_bus,
        B.name AS arret_inter,
        D.route_name AS deuxieme_bus,
        E.name AS destination
    FROM 
        network_nodes_belfast AS A,
        routes_bus_belfast AS F,
        routes_belfast AS C,
        routes_bus_belfast AS G,
        network_nodes_belfast AS B,
        routes_bus_belfast AS H,
        routes_belfast AS D,
        routes_bus_belfast AS I,
        network_nodes_belfast AS E
    WHERE 
        A.stop_i = F.stop_i
        AND F.route_i = C.route_i
        AND G.route_i = F.route_i
        AND G.stop_i = B.stop_i
        AND B.stop_i = H.stop_i
        AND H.route_i = D.route_i
        AND I.route_i = H.route_i
        AND I.stop_i = E.stop_i
        AND A.name = '{_fromstation}'
        AND E.name = '{_tostation}'
        AND A.stop_i <> B.stop_i 
        AND B.stop_i <> E.stop_i
        AND C.route_name <> D.route_name;
""")


            self.conn.commit()
            rows += self.cursor.fetchall()
        if _hops == 3 :
            if _hops == 3:
    self.cursor.execute("""
        SELECT DISTINCT
            A.name AS departure_station,
            A.route_i AS route_to_intermediate_1,
            B.name AS intermediate_station_1,
            B.route_i AS route_to_intermediate_2,
            C.name AS intermediate_station_2,
            C.route_i AS route_to_destination,
            D.name AS destination
        FROM 
            network_nodes_with_routes AS A,
            network_nodes_with_routes AS B,
            network_nodes_with_routes AS C,
            network_nodes_with_routes AS D 
        WHERE 
            A.name = '{_fromstation}'
            AND D.name = '{_tostation}'
            AND A.stop_i <> B.stop_i
            AND B.stop_i <> C.stop_i
            AND C.stop_i <> D.stop_i
            AND A.route_i <> B.route_i
            AND A.route_i <> C.route_i
            AND B.route_i <> C.route_i
    """)



            self.conn.commit()
            rows += self.cursor.fetchall()
        if len(rows) == 0 : 
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[-1]))

        i = 0
        for row in rows : 
            j = 0
            for col in row :
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))
                j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < len(rows[-1]) :
            header.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)
            j = j+1
        
        self.update()	


    def button_Distance(self):
        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        distance = self.calculate_actual_distance(_fromstation, _tostation)

        if distance != "Distance not found":
            QtWidgets.QMessageBox.information(self, "Distance", f"Distance between {_fromstation} and {_tostation}: {distance}")
        else:
            QtWidgets.QMessageBox.information(self, "Distance", "Distance not found or calculation failed.")

    def calculate_actual_distance(self, from_station, to_station):
        query = """
            SELECT
                6371 * ACOS(
                    COS(RADIANS(A.lat)) * COS(RADIANS(B.lat)) *
                    COS(RADIANS(B.lon) - RADIANS(A.lon)) +
                    SIN(RADIANS(A.lat)) * SIN(RADIANS(B.lat))
                ) AS distance_km
            FROM
                network_nodes_belfast A
                CROSS JOIN network_nodes_belfast B
            WHERE
                A.name = %s
                AND B.name = %s;
        """
        self.cursor.execute(query, (from_station, to_station))
        result = self.cursor.fetchone()

        if result and result[0] is not None:
            return round(result[0], 2)  
        else:
            return "Distance not found"

    
    def button_Duration(self):
        query = """
            SELECT DISTINCT
   a.name, d.name,
   b.arr_time_ut - b.dep_time_ut AS journey_duration
FROM 
    network_temporal_day_belfast as b, network_nodes_belfast as a, network_nodes_belfast as d 
where a.stop_i=b.from_stop_i AND d.stop_i=b.to_stop_i and b.arr_time_ut-b.dep_time_ut <>0 and a.name <> d.name;
        """
        self.cursor.execute(query)
        durations = self.cursor.fetchall()

        if durations:
            self.tableWidget.setRowCount(len(durations))
            self.tableWidget.setColumnCount(len(durations[0]))

            for i, row in enumerate(durations):
                for j, col in enumerate(row):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))
        else:
            QtWidgets.QMessageBox.information(self, "Durations", "No durations found.")


    def table_Click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())       
        




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
