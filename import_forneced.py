import pandas as pd
from main import app, db
from models import Fornecedores

with app.app_context():
    file_path = r'C:\Pasta1.xlsx'

    df = pd.read_excel(file_path, skiprows=1, header=None, names=['Codigo', 'RAZAOSOCIA'])

    for index, row in df.iterrows():
        fornecedor = Fornecedores(
            fornecedCnpj=row['Codigo'],
            fornecedRazaoSocial=row['RAZAOSOCIA']
        )
        db.session.add(fornecedor)

    db.session.commit()

    print("Dados importados com sucesso")