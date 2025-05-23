import sys
import time
from PySide6 import QtWidgets
from ui.telaEmpresa import EmpresaWindow
from utils.icone import usar_icone

def main():
    inicio = time.time()

    app = QtWidgets.QApplication(sys.argv)
    
    janela = EmpresaWindow()
    usar_icone(janela)
    janela.showMaximized()

    fim = time.time()
    print(f"[DEBUG] Tempo de abertura da janela inicial: {fim - inicio:.2f} segundos")

    sys.exit(app.exec())

if __name__ == '__main__':
    main()