# IMPORTANDO BIBLIOTECA JSON

import json

# GUARDANDO ARQUIVOS DE CADA SEGMENTO EM UMA VARIÁVEL

estudantes="estudantes.json"
disciplinas="disciplinas.json"
professores="professores.json"
turmas="turmas.json"
matriculas="matriculas.json"

# INÍCIO DAS FUNÇÕES

# FUNÇÃO PARA LER ARQUIVOS E RETORNAR NUMA VARIÁVEL "LISTA" OU LISTA VAZIA
def read_json(arquivo):
    try:
        with open(arquivo,"r") as f:
            lista=json.load(f)
            return lista
    except FileNotFoundError:
        return []

# FUNÇÃO PARA ESCREVER ARQUIVOS, OU SEJA, ATUALIZAR E SALVAR NOVAMENTE NO ARQUIVO JSON
def write_json(lista,arquivo):
    with open(arquivo,"w") as f:
        json.dump(lista,f,indent=4, ensure_ascii=False)

# FUNÇÃO PARA CORRIGIR ERROS DE VALUE ERROR, STR PARA INT
def error():
    while True:
        try:
            num = int(input("Digite a opção desejada: "))
            return num
        except ValueError:
            print("Somente números são válidos.\n")
            continue

# FUNÇÃO PARA CORRIGIR ERROS DE VALUE ERROR, STR PARA INT
def error1(nome):
    while True:
        try:
            cod=int(input(f"Digite o código do(a) {nome}: "))
            return cod
        except ValueError:
            print("Somente números são válidos.\n")
            continue

# FUNÇÃO PARA MOSTRAR O MENU PRINCIPAL AO USUÁRIO
def main_menu():
    print("\nMENU PRINCIPAL\n")
    print("1. ESTUDANTES")
    print("2. DISCIPLINAS")
    print("3. PROFESSORES")
    print("4. TURMAS")
    print("5. MATRÍCULAS")
    print("6. SAIR\n")
    e=error()
    return e

# FUNÇÃO PARA MOSTRAR O MENU SECUNDÁRIO AO USUÁRIO
def second_menu():
    print("\nMENU DE OPERAÇÕES\n")
    print("1. INCLUIR")
    print("2. LISTAR")
    print("3. EDITAR")
    print("4. EXCLUIR")
    print("5. VOLTAR AO MENU PRINCIPAL\n")
    e=error()
    return e

# FUNÇÃO PARA INCLUIR ESTUDANTES, DISCIPLINAS, PROFESSORES, TURMAS E MATRÍCULAS
def incluir(arquivo,campos,nome):
    lista = read_json(arquivo)
    print(f"\nINCLUIR {nome.upper()}\n")

    if campos in [estudantes,professores,disciplinas,turmas]:
        cod = error1(nome)
        existe = False
        for item in lista:
            if item["Código"] == cod:
                print(f"{nome.capitalize()} já existe.")
                return
        if not existe:
            if campos in [estudantes,professores]:
                nome_ = input(f"Digite o nome do(a) {nome}: ")
                cpf=input(f"Digite o CPF do(a) {nome}: ")
                novo_registro={"Código":cod,"Nome":nome_, "CPF":cpf}
                lista.append(novo_registro)
                write_json(lista, arquivo)
                print(f"\n{nome.capitalize()} incluído com sucesso!")
                return

            elif campos == disciplinas:
                nome_ = input(f"Digite o nome do(a) {nome}: ")
                novo_registro_d = {"Código": cod, "Nome": nome_}
                lista.append(novo_registro_d)
                write_json(lista, arquivo)
                print(f"\n{nome.capitalize()} incluída com sucesso!")
                return

            elif campos == turmas:
                lista_professores = read_json(professores)
                lista_disciplinas = read_json(disciplinas)
                cod_prof = None
                cod_disc = None
                while True:
                    try:
                        cod_prof = int(input("Digite o código do professor: "))
                        break
                    except ValueError:
                        print("Somente números são válidos.\n")
                        continue
                for item in lista_professores:
                    if item["Código"] == cod_prof:
                        while True:
                            try:
                                cod_disc = int(input("Digite o código da disciplina: "))
                                break
                            except ValueError:
                                print("Somente números são válidos.\n")
                                continue
                        for item in lista_disciplinas:
                            if item["Código"] == cod_disc:
                                novo_registro_t = {"Código": cod, "Professor": cod_prof, "Disciplina": cod_disc}
                                lista.append(novo_registro_t)
                                write_json(lista, arquivo)
                                print(f"\n{nome.capitalize()} incluído(a) com sucesso!")
                                return
                        else:
                            print("\nDisciplina não encontrada.")
                            return
                else:
                    print("\nProfessor não encontrado.")
                    return
    elif campos == matriculas:
        lista_turmas = read_json(turmas)
        lista_estudantes = read_json(estudantes)
        cod_t = None
        cod_e = None
        while True:
            try:
                cod_t = int(input("Digite o código da turma: "))
                break
            except ValueError:
                print("Somente números são válidos.\n")
                continue
        existe_turma = False
        for turma in lista_turmas:
            if turma["Código"] == cod_t:
                existe_turma = True
        if not existe_turma:
            print("\nTurma não existe.")
            return
        while True:
            try:
                cod_e = int(input("Digite o código do estudante: "))
                break
            except ValueError:
                print("Somente números são válidos.\n")
                continue
        existe_est = False
        for est in lista_estudantes:
            if est["Código"] == cod_e:
                existe_est = True
                break
        if not existe_est:
            print("\nEstudante não existe.")
            return
        for item in lista:
            if item["Estudante"] == cod_e:
                print("\nEstudante já cadastrado com outra matrícula.")
                return
        nova_m = {"Turma":cod_t,"Estudante":cod_e}
        lista.append(nova_m)
        write_json(lista,arquivo)
        print(f"\n{nome.capitalize()} incluída com sucesso!")
        return

# FUNÇÃO PARA LISTAR ESTUDANTES, DISCIPLINAS, PROFESSORES, TURMAS E MATRÍCULAS
def listar(arquivo,nome):
    lista = read_json(arquivo)
    print(f"\nLISTAR {nome.upper()}\n")
    if not lista:
        print(f"Não há cadastros de {nome}.")
        return
    if lista:
        for item in lista:
            for chave,valor in item.items():
                print(f"{chave}: {valor}")
            print()

# FUNÇÃO PARA EDITAR ESTUDANTES E PROFESSORES
def editar_estudantes_e_professores(arquivo,nome):
    lista = read_json(arquivo)
    if not lista:
        print(f"Não há cadastros de {nome}.")
        return
    print(f"\nEDITAR {nome.upper()}\n")
    novo_cod = None
    cod = error1(nome)
    for item in lista:
        if item["Código"] == cod:
            while True:
                try:
                    novo_cod = int(input(f"Digite o novo código do {nome}: "))
                    break
                except ValueError:
                    print("Somente números são válidos.")
                    continue
            for outro in lista:
                if outro["Código"] == novo_cod and outro != item:
                    print(f"{nome.capitalize()} já existe.")
                    return
            item["Código"] = novo_cod
            item["Nome"] = input(f"Digite o novo nome do {nome}: ")
            item["CPF"] = input(f"Digite o novo CPF do {nome}: ")
            write_json(lista, arquivo)
            print(f"{nome.capitalize()} editado com sucesso!")
            return
    print(f"{nome.capitalize()} não existe.")
    return

# FUNÇÃO PARA EDITAR DISCIPLINAS
def editar_disciplinas(arquivo,nome):
    lista = read_json(arquivo)
    if not lista:
        print(f"Não há cadastros de {nome}.")
        return
    print(f"\nEDITAR {nome.upper()}\n")
    cod = error1(nome)
    item = None
    existe = False
    for item in lista:
        if item["Código"] == cod:
            existe = True
            break
    if not existe:
        print("Disciplina não existe.")
        return
    novo_cod = int(input("Digite o novo código da disciplina: "))
    existe_novo = False
    for outro in lista:
        if outro["Código"] == novo_cod:
            print("Disciplina com esse código já existe.")
            return
    if not existe_novo:
        item["Código"] = novo_cod
        item["Nome"] = input("Digite o novo nome da disciplina: ")
        write_json(lista, arquivo)
        print("Disciplina editada com sucesso!")
        return

# FUNÇÃO PARA EDITAR TURMAS
def editar_turmas(arquivo,nome):
    lista = read_json(arquivo)
    lista_prof = read_json(professores)
    lista_disc = read_json(disciplinas)
    if not lista:
        print(f"Não há cadastros de {nome}.")
        return
    print(f"\nEDITAR {nome.upper()}\n")
    cod = error1(nome)
    novo_cod = None
    item = None
    novo_prof = None
    novo_disc = None
    existe_turma = False
    for item in lista:
        if item["Código"] == cod:
            existe_turma = True
            break
    if not existe_turma:
        print(f"{nome.capitalize()} não existe.")
        return
    while True:
        try:
            novo_cod = int(input("Digite o novo código da turma: "))
            break
        except ValueError:
            print("Somente números são válidos.")
            continue
    existe_novo_cod = False
    for outro in lista:
        if outro["Código"] == novo_cod:
            print(f"{nome.capitalize()} já existe.")
            return
    if not existe_novo_cod:
        item["Código"] = novo_cod
        while True:
            try:
                novo_prof = int(input("Digite o código do novo professor: "))
                break
            except ValueError:
                print("Somente números são válidos.")
                continue
        existe_prof = False
        for prof in lista_prof:
            if prof["Código"] == novo_prof:
                existe_prof = True
                break
        if not existe_prof:
            print("Professor não existe.")
            return
        item["Professor"] = novo_prof
        while True:
            try:
                novo_disc = int(input("Digite o código da nova disciplina: "))
                break
            except ValueError:
                print("Somente números são válidos.")
                continue
        existe_disc = False
        for disc in lista_disc:
            if disc["Código"] == novo_disc:
                existe_disc = True
                break
        if not existe_disc:
            print("Disciplina não existe.")
            return
        item["Disciplina"] = novo_disc
        write_json(lista, arquivo)
        print("Turma editada com sucesso!")
        return

# FUNÇÃO PARA EDITAR MATRÍCULAS
def editar_matriculas(arquivo,nome):
    lista = read_json(arquivo)
    lista_turmas = read_json(turmas)
    lista_est = read_json(estudantes)
    if not lista:
        print(f"Não há cadastros de {nome}.")
        return
    print(f"\nEDITAR {nome.upper()}\n")
    cod_t = None
    cod_est = None
    cod_nova_t = None
    while True:
        try:
            cod_t = int(input("Digite o código da turma atual: "))
            break
        except ValueError:
            print("Somente números são válidos.")
            continue
    existe_t = False
    for turma in lista_turmas:
        if turma["Código"] == cod_t:
            existe_t = True
            break
    if not existe_t:
        print("Turma não existe.")
        return
    while True: # TURMA EXISTE
        try:
            cod_est = int(input("Digite o código do estudante atual: "))
            break
        except ValueError:
            print("Somente números são válidos.")
            continue
    existe_est = False
    for est in lista_est:
        if est["Código"] == cod_est:
            existe_est = True
            break
    if not existe_est:
        print("Estudante não existe.")
        return
    for mat in lista: # ESTUDANTE EXISTE
        if mat["Turma"] == cod_t and mat["Estudante"] == cod_est: # ENCONTRAMOS A MATRÍCULA
            while True:
                try:
                    cod_nova_t = int(input("Digite o código da nova turma: "))
                    break
                except ValueError:
                    print("Somente números são válidos.")
                    continue
            for turma in lista_turmas:
                if turma["Código"] == cod_nova_t:
                    mat["Turma"] = cod_nova_t # SUBSTITUINDO TURMA NA MATRÍCULA ENCONTRADA
                    write_json(lista, arquivo)
                    print(f"{nome.capitalize()} editada com sucesso!")
                    return
            print("Turma não existe.")
            return
    print("Matrícula não existe.")
    return

# FUNÇÃO PARA EXCLUIR ESTUDANTES, DISCIPLINAS, PROFESSORES, TURMAS E MATRÍCULAS
def excluir(arquivo,campos,nome):
    lista = read_json(arquivo)
    if not lista:
        print(f"\nNão há cadastros de {nome}.")
        return
    print(f"\nEXCLUIR {nome.upper()}\n")
    if campos in [estudantes,disciplinas,professores,turmas]:
        while True:
            cod = error1(nome)
            existe = False
            for item in lista:
                if item["Código"] == cod:
                    lista.remove(item)
                    write_json(lista, arquivo)
                    print(f"\n{nome.capitalize()} excluído(a) com sucesso!")
                    return
            if not existe:
                print(f"\nNão há cadastro de {nome} com esse código.")
                return
    elif campos == matriculas:
        lista_t = read_json(turmas)
        lista_e = read_json(estudantes)
        item = None
        cod_t = None
        cod_e = None
        while True:
            try:
                cod_t = int(input(f"Digite o código da turma: "))
                break
            except ValueError:
                print("Somente números são válidos.\n")
                continue
        existe1 = False
        for turma in lista_t:
            if turma["Código"] == cod_t:
                existe1 = True
                break
        if not existe1:
            print("\nTurma não existe.")
            return
        i = False
        for item in lista:
            if item["Turma"] == cod_t:
                i = True
                break
        if not i:
            print("\nTurma não cadastrada com essa matrícula.")
            return
        while True:
            try:
                cod_e = int(input("Digite o código do estudante: "))
                break
            except ValueError:
                print("Somente números são válidos.\n")
                continue
        existe2 = False
        for est in lista_e:
            if est["Código"] == cod_e:
                existe2 = True
                break
        if not existe2:
            print("\nEstudante não existe.")
            return
        i2 = False
        for item in lista:
            if item["Estudante"] == cod_e:
                i2 = True
                break
        if not i2:
            print("\nEstudante não cadastrado com essa matrícula.")
            return
        lista.remove(item)
        write_json(lista, arquivo)
        print(f"\n{nome.capitalize()} excluído(a) com sucesso!")
        return

# CÓDIGO PRINCIPAL

def main():
    while True:
        option1 = main_menu()
        if option1 == 6:
            print("\nEncerrando...")
            break
        if option1 not in [1,2,3,4,5]:
            print("Digite um número válido.")
            continue
        while True:
            option2 = second_menu()
            if option1 == 1:
                if option2 == 1:
                    incluir(estudantes,estudantes,"estudante")
                elif option2 == 2:
                    listar(estudantes,"estudante")
                elif option2 == 3:
                    editar_estudantes_e_professores(estudantes,"estudante")
                elif option2 == 4:
                    excluir(estudantes,estudantes,"estudante")
                elif option2 == 5:
                    print("\nVoltando ao Menu Principal...")
                    break
                else:
                    print("Digite um número válido.")
                    continue
            elif option1 == 2:
                if option2 == 1:
                    incluir(disciplinas,disciplinas,"disciplina")
                elif option2 == 2:
                    listar(disciplinas,"disciplina")
                elif option2 == 3:
                    editar_disciplinas(disciplinas,"disciplina")
                elif option2 == 4:
                    excluir(disciplinas,disciplinas,"disciplina")
                elif option2 == 5:
                    print("\nVoltando ao Menu Principal...")
                    break
                else:
                    print("Digite um número válido.")
                    continue
            elif option1 == 3:
                if option2 == 1:
                    incluir(professores,professores,"professor")
                elif option2 == 2:
                    listar(professores,"professor")
                elif option2 == 3:
                    editar_estudantes_e_professores(professores,"professor")
                elif option2 == 4:
                    excluir(professores,professores,"professor")
                elif option2 == 5:
                    print("\nVoltando ao Menu Principal...")
                    break
                else:
                    print("Digite um número válido.")
                    continue
            elif option1 == 4:
                if option2 == 1:
                    incluir(turmas,turmas,"turma")
                elif option2 == 2:
                    listar(turmas,"turma")
                elif option2 == 3:
                    editar_turmas(turmas,"turma")
                elif option2 == 4:
                    excluir(turmas,turmas,"turma")
                elif option2 == 5:
                    print("\nVoltando ao Menu Principal...")
                    break
                else:
                    print("Digite um número válido.")
                    continue
            elif option1 == 5:
                if option2 == 1:
                    incluir(matriculas,matriculas,"matrícula")
                elif option2 == 2:
                    listar(matriculas,"matrícula")
                elif option2 == 3:
                    editar_matriculas(matriculas,"matrícula")
                elif option2 == 4:
                    excluir(matriculas,matriculas,"matrícula")
                elif option2 == 5:
                    print("\nVoltando ao Menu Principal...")
                    break
                else:
                    print("Digite um número válido.")
                    continue
            else:
                print("Digite um número válido.")
                continue
if __name__ == "__main__":
    main()