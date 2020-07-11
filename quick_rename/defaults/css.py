CSS = """
QWidget {
    background-color: #b5c0c9;
    font-weight: normal;
    font-size: 1em;
    font-weight: 500;
    color: #000000; 
}

QFrame {
    background-color: #b5c0c9;
    border: 2px solid #81888f;
    border-radius: 6px;
}

QPushButton {
    background-color: #b5c0c9;
    border: 1px solid #81888f;
    border-radius: 3px;
    height:2em;
    padding-left: 10px;
    padding-right: 10px;
}

QCheckBox::indicator {
    background-color: #b5c0c9;
    border: 1px solid #81888f;
    border-radius: 12px;
    height:1em;
    width: 1em;
}

QCheckBox::indicator::unchecked::hover {
    background-color: #dea621
}

QCheckBox::indicator::checked {
    background-color: #81bef0;
}

QScrollBar {
    background: transparent;
}

QScrollBar::handle {
    background: #8b969e;
}

QHeaderView {
    background-color: #a0aeba;
    border: none;
    border-radius: 6px;
}

QHeaderView::section {
    background-color: #a0aeba;
    font-weight: bold;
    font-size: 1.2em;
    height: 2em;
    border: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTableView {
    alternate-background-color: #a0aeba;
    border: 2px solid #81888f;
    border-radius: 6px;
}


QTableView::indicator {
    border: 1px solid #81888f;
    border-radius: 12px;
    height:1em;
    width: 1em;
}

QTableView::indicator::unchecked::hover {
    background-color: #dea621
}
QTableView::indicator::checked {
    background-color: #81bef0;
}

QPushButton::hover{
    background-color: #81bef0;
}

QLineEdit{
    background-color: #81bef0;
    border: 2px solid #81888f;
    border-radius: 6px;
    color: #000000; 
    height:2em;
    padding-left: 10px;
    padding-right: 10px;
}

QLineEdit::disabled{
    background-color: #8b969e;
}

QLabel {
    color: #000000;
    border: 0px solid #000;  
}

QLabel#instructions{
    color: gray;
    font-weight: normal;
    font-size: .5em;
    v-align: center;
}
"""
