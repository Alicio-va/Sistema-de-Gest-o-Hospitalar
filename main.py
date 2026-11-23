from collections import deque #Importa o deque,permitindo traalhar com filas
import os #Importa uma bilioteca python, utilizada para verificar se um arquivo existe

arquivo = "dados_sistema.txt"

lista_pacientes = [] #Lista vazia para adicionar pacientes
fila_triagem = deque() #Fila vazia para organizar os pacientes
pilha_prontuarios = [] #Lista vazia que será utilizada como pilha de prontuários
arvore_especialidades = {} #Dicionário vazio que será utilizado para as especiaidades e diagnósticos


## Função utilizada para receber informações e verificar se o campo está preenchido corretamente
def ler_campo(mensagem): #Cria a função "ler_campo" que recebe uma mensagem do usuário
  while True: #Repetição contínua
    valor = input(mensagem).strip() #Remove espaços em branco

    if valor == "": #Verifica se o campo está vazio
      print("O campo não pode ficar vazio.")

#Impede a utilização do caracter "|", pois está sendo usado para separar as informações no arquivo.txt
    elif "|" in valor: 
      print("Não utilize o caractere |.")

    else:
      return valor

## Cadastra um paciente na lista, verificando se o ID já existe
def cadastrar_paciente(): #Função responsavel pelo cadastro
  print("\n==== CADASTRAR PACIENTE ====")

  id_paciente = ler_campo("Informe o ID do paciente: ")

  encontrado = False #Considera que o ID ainda não foi encontrado

  for paciente in lista_pacientes: #Percorre todos os pacientes que já estão cadastrados
    if paciente["id"] == id_paciente: #Compara os IDs
      encontrado = True #Altera para "True" caso o ID seja encontrado

  if encontrado: #Verifica se o ID existe
    print("ID já cadastrado.")

  else:
    nome = ler_campo("Informe o nome do paciente: ")
    leito = ler_campo("Informe o número do leito: ")
    status = ler_campo("Informe o status do paciente: ")
    doenca = ler_campo("Informe a doença: ")

    paciente = {
        "id": id_paciente,
        "nome": nome,
        "leito": leito,
        "status": status,
        "doenca": doenca
    }

    lista_pacientes.append(paciente) #Adiciona o dicionário do paciente no final da lista

    print("Paciente cadastrado com sucesso!")

## Procura um paciente pelo ID e exibe suas informações
def consultar_paciente(): #Função de consulta
  print("\n==== CONSULTAR PACIENTE ====")

  id_paciente = input("Informe o ID do paciente: ") #Solicita o ID que será pesquisado
  encontrado = False

  for paciente in lista_pacientes: #Percorre a lista em usca do paciente informado
    if paciente["id"] == id_paciente: #Verifica se o ID do paciente bate com o informado
      print("\nID:", paciente["id"])
      print("Nome:", paciente["nome"])
      print("Leito:", paciente["leito"])
      print("Status:", paciente["status"])
      print("Doença:", paciente["doenca"])

      encontrado = True
      break #Interrompe a repetição quando o paciente é encontrado

  if not encontrado: #Caso a variável continua sendo falsa
    print("Paciente não encontrado.")

## Localiza o paciente pelo ID e permite alterar suas informações
def atualizar_paciente(): #Função de atualização 
  print("\n==== ATUALIZAR PACIENTE ====")

  id_paciente = input("Informe o ID do paciente: ") #Solicita o ID que será alterado
  encontrado = False

  for paciente in lista_pacientes: #Percorre os pacientes
    if paciente["id"] == id_paciente: #Verifica se encontrou o paciente
      encontrado = True

      print("\n1- Alterar nome")
      print("2- Alterar leito")
      print("3- Alterar status")
      print("4- Alterar doença")

      opcao = input("Escolha uma opção: ")

      if opcao == "1":
        paciente["nome"] = ler_campo("Novo nome: ") #Sustitui o nome antigo pelo novo
        print("Nome atualizado!")

      elif opcao == "2":
        paciente["leito"] = ler_campo("Novo leito: ")
        print("Leito atualizado!")

      elif opcao == "3":
        paciente["status"] = ler_campo("Novo status: ")
        print("Status atualizado!")

      elif opcao == "4":
        paciente["doenca"] = ler_campo("Nova doença: ")
        print("Doença atualizada!")

      else: #Informa qaundo a opção escolhida não existe
        print("Opção inválida.")

      break

  if not encontrado: #Informa se o ID não for localizado
    print("Paciente não encontrado.")

## Percorre a lista pelo índice e remove o paciente que possui o ID informado
def excluir_paciente(): #Função de exclusão
  print("\n==== EXCLUIR PACIENTE ====")

  id_paciente = input("Informe o ID do paciente: ") #Solicita ID do paciente
  encontrado = False

#range() Percorre as posições na lista, usando os numeros dos índices
  for i in range(len(lista_pacientes)): #len(), informa quantos elementos existem na lista
    if lista_pacientes[i]["id"] == id_paciente: #Verifica se o ID corresponde ao informado
      lista_pacientes.pop(i) #Remove o paciente da posição encontrada

      print("Paciente excluído com sucesso!")
      encontrado = True
      break

  if not encontrado:
    print("Paciente não encontrado.")

## Verifica se existem pacientes cadastrados e exibe todos os registros
def listar_pacientes(): #Função de listagem
  print("\n==== PACIENTES INTERNADOS ====")

  if len(lista_pacientes) == 0: #Verifica se a lista esta vazia
    print("Não existem pacientes cadastrados.")

  else: #Executa quando existem pacientes cadastrados
    for paciente in lista_pacientes:
      print("\nID:", paciente["id"])
      print("Nome:", paciente["nome"])
      print("Leito:", paciente["leito"])
      print("Status:", paciente["status"])
      print("Doença:", paciente["doenca"])

## Menu responsável por acessar as operações da lista de pacientes
def menu_pacientes():
  while True:
    print("\n===== PACIENTES INTERNADOS =====")
    print("1- Cadastrar paciente")
    print("2- Consultar paciente")
    print("3- Atualizar informações")
    print("4- Excluir paciente")
    print("5- Listar pacientes")
    print("0- Voltar")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
      cadastrar_paciente()

    elif opcao == "2":
      consultar_paciente()

    elif opcao == "3":
      atualizar_paciente()

    elif opcao == "4":
      excluir_paciente()

    elif opcao == "5":
      listar_pacientes()

    elif opcao == "0":
      break

    else:
      print("Opção inválida!")

## Adiciona um novo paciente ao final da fila de triagem
def adicionar_fila(): #Função para adicionar pacientes na fila
  print("\n==== ADICIONAR PACIENTE NA FILA ====")

  id_paciente = ler_campo("ID do paciente: ") #Recebe o ID do paciente

  nome = ler_campo("Nome do paciente: ") #Recebe o nome
  prioridade = ler_campo("Prioridade do caso: ") #Informa a prioridade

  paciente = { #Organiza as informações em um dicionário
      "id": id_paciente,
      "nome": nome,
      "prioridade": prioridade
  }

  fila_triagem.append(paciente) #Adiciona um paciente no final da fila

  print("Paciente adicionado ao final da fila!")

## Remove o primeiro paciente da fila, respeitando a regra FIFO
def atender_paciente(): #Função de atendimento
  print("\n==== ATENDER PACIENTE ====")

  if len(fila_triagem) == 0: #Verifica a fila vazia
    print("Não existem pacientes aguardando.")

  else: #Executa quando houver pacientes
    atendido = fila_triagem.popleft() #Remove o primeiro paciente da fila, guardando suas informações

    print("Paciente atendido:", atendido["nome"])
    print("ID:", atendido["id"])
    print("Prioridade:", atendido["prioridade"])

    print("Atendimento realizado com sucesso!")

## Exibe os pacientes que estão aguardando atendimento na fila
def consultar_fila(): #Função para visualizar a fila
  print("\n==== FILA DE TRIAGEM ====")

  if len(fila_triagem) == 0: #Verifica se a fila esta vazia
    print("Fila vazia.")

  else: #Executa quando houver alguém na fila
    print("Quantidade de pacientes:", len(fila_triagem)) #Informa a quantidade de pacientes aguardando

    for paciente in fila_triagem: #Percorre os pacientes da fila
      print( 
          paciente["id"],
          "-",
          paciente["nome"],
          "-",
          paciente["prioridade"]
      )

## Localiza o paciente pelo ID e permite atualizar suas informações sem alterar sua posição na fila
def atualizar_fila(): #Função de atualização
  print("\n==== ATUALIZAR PACIENTE DA FILA ====")

  id_paciente = input("Informe o ID do paciente: ") #Recebe ID do paciente que será alterado
  encontrado = False

  for paciente in fila_triagem: #Percorre os pacientes da fila
    if paciente["id"] == id_paciente: #Verifica se encontrou o paciente
      encontrado = True

      print("1- Alterar nome")
      print("2- Alterar prioridade")

      opcao = input("Escolha uma opção: ")

      if opcao == "1":
        paciente["nome"] = ler_campo("Novo nome: ")
        print("Nome atualizado!")

      elif opcao == "2":
        paciente["prioridade"] = ler_campo("Nova prioridade: ")
        print("Prioridade atualizada!")

      else:
        print("Opção inválida.")

      break

  if not encontrado: #Informa se o paciente não for encontrado
    print("Paciente não encontrado.")

## Menu responsável por acessar as operações da fila de triagem
def menu_fila():
  while True:
    print("\n===== FILA DE TRIAGEM =====")
    print("1- Adicionar paciente")
    print("2- Atender próximo paciente")
    print("3- Consultar fila")
    print("4- Atualizar paciente")
    print("5- Consultar quantidade")
    print("0- Voltar")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
      adicionar_fila()

    elif opcao == "2":
      atender_paciente()

    elif opcao == "3":
      consultar_fila()

    elif opcao == "4":
      atualizar_fila()

    elif opcao == "5":
      print("Quantidade de pacientes:", len(fila_triagem))

    elif opcao == "0":
      break

    else:
      print("Opção inválida!")

## Registra um novo acesso e adiciona o prontuário ao topo da pilha
def adicionar_prontuario(): #Cria a função de registro
  print("\n==== ACESSAR PRONTUÁRIO ====")

  id_prontuario = ler_campo("ID do prontuário: ") #Recebe o identificador do prontuário
  id_paciente = ler_campo("ID do paciente: ") #Recebe o ID do paciente
  especialidade = ler_campo("Especialidade médica: ") #Recebe a especialidade do médico

  prontuario = { #Organiza as informações em um dicionário
      "id": id_prontuario,
      "paciente": id_paciente,
      "especialidade": especialidade
  }

  pilha_prontuarios.append(prontuario) #Adiciona o prontuário ao topo da pilha

  print("Prontuário adicionado ao histórico!")

## Consulta o prontuário que está no topo da pilha, sem removê-lo
def consultar_prontuario(): #Cria a função de consulta
  print("\n==== PRONTUÁRIO MAIS RECENTE ====")

  if len(pilha_prontuarios) == 0: #Verifica se a pilha esta vazia
    print("Não existem prontuários no histórico.")

  else: #Executa quando existem prontuários
    prontuario = pilha_prontuarios[-1]  #Acessa o ultimo elemento da lista, que é o topo da pilha
                                        #[-1] representa o ultimo elemento da lista

    print("ID:", prontuario["id"])
    print("Paciente:", prontuario["paciente"])
    print("Especialidade:", prontuario["especialidade"])

## Percorre a pilha de trás para frente para exibir primeiro os prontuários mais recentes
def listar_prontuarios(): #Cria a função de histórico
  print("\n==== HISTÓRICO DE PRONTUÁRIOS ====")

  if len(pilha_prontuarios) == 0: #Verifica se a pilha está vazia
    print("Histórico vazio.")

  else: #Executa quando houver prontuários
    #Conta quantos prontuários existem
    #O primeiro -1: Encontra o indice do último elemento
    #O segundo -1: Indica que a repetição deve chegar até antes do índice -1
    #O terceiro -1: Indica que a contagem deve ser feita de tras pra frente
    for i in range(len(pilha_prontuarios) - 1, -1, -1):
      prontuario = pilha_prontuarios[i]

      print("\nID:", prontuario["id"])
      print("Paciente:", prontuario["paciente"])
      print("Especialidade:", prontuario["especialidade"])

## Permite atualizar as informações do prontuário que está no topo da pilha
def atualizar_prontuario(): #Cria a função de atulização
  print("\n==== ATUALIZAR PRONTUÁRIO ====")

  if len(pilha_prontuarios) == 0: #Verifica se a pilha esta vazia
    print("Histórico vazio.")

  else: #Executa quando existe prontuários
    prontuario = pilha_prontuarios[-1] #Acessa somente o prontuário do topo

    print("Prontuário do topo:", prontuario["id"])
    print("1- Alterar ID do paciente")
    print("2- Alterar especialidade")

    opcao = input("Escolha uma opção: ")

    if opcao == "1": #Permite alterar o ID do paciente
      prontuario["paciente"] = ler_campo("Novo ID do paciente: ")
      print("Prontuário atualizado!")

    elif opcao == "2": #Permite alterar a especialidade médica
      prontuario["especialidade"] = ler_campo("Nova especialidade: ")
      print("Prontuário atualizado!")

    else: #Informa quando a opção é inválida
      print("Opção inválida.")

## Remove o prontuário que está no topo da pilha, seguindo a regra LIFO
def remover_prontuario(): #Cria a função de remoção
  print("\n==== REMOVER PRONTUÁRIO ====")

  if len(pilha_prontuarios) == 0: #Verifica se a pilha está vazia
    print("Histórico vazio.")

  else: #Executa quando houver prontuários
    removido = pilha_prontuarios.pop() #Remove o ultimo elemento da lista, ou seja, o topo da pilha

    print("Prontuário removido:", removido["id"]) #Mostra o prontuário que foi removido

## Menu responsável por acessar as operações da pilha de prontuários
def menu_prontuarios():
  while True:
    print("\n===== HISTÓRICO DE PRONTUÁRIOS =====")
    print("1- Registrar acesso")
    print("2- Consultar último acesso")
    print("3- Listar histórico")
    print("4- Atualizar último acesso")
    print("5- Remover último acesso")
    print("0- Voltar")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
      adicionar_prontuario()

    elif opcao == "2":
      consultar_prontuario()

    elif opcao == "3":
      listar_prontuarios()

    elif opcao == "4":
      atualizar_prontuario()

    elif opcao == "5":
      remover_prontuario()

    elif opcao == "0":
      break

    else:
      print("Opção inválida!")

## Adiciona uma nova especialidade à árvore, evitando cadastros duplicados
def adicionar_especialidade(): #Cria a função de cadastro de especialidade
  print("\n==== CADASTRAR ESPECIALIDADE ====")

  especialidade = ler_campo("Nome da especialidade: ") #Recebe o nome da especialidade

  if especialidade in arvore_especialidades: #Verifica se a especialidade ja esta cadastrada
    print("Especialidade já cadastrada.")

  else: #Executa caso ainda não esteja
    arvore_especialidades[especialidade] = {} #Adiciona a especialidade como uma chave, criando um dicionário vazio dentro dela

    print("Especialidade cadastrada!")

## Cadastra um diagnóstico dentro da especialidade correspondente
def adicionar_diagnostico(): #Cria a função de cadastro de diagnóstico
  print("\n==== CADASTRAR DIAGNÓSTICO ====")

  especialidade = ler_campo("Informe a especialidade: ") #Recebe a especialidade desejada

  if especialidade in arvore_especialidades: #Verifica se a especialidade informada existe
    diagnostico = ler_campo("Informe o diagnóstico: ") #Recebe o nome do diagnóstico

    if diagnostico in arvore_especialidades[especialidade]: #Verifica se o diagnóstico já existe dentro da arvore da especialidade
      print("Diagnóstico já cadastrado.")

    else: #Executa se o diagnóstico ainda não foi cadastrado
      arvore_especialidades[especialidade][diagnostico] = {} #Adiciona o diagnóstico dentro da especialidade informada

      print("Diagnóstico cadastrado!")

  else: #Informa quando a especialidade não existe
    print("Especialidade não encontrada.")

## Percorre a árvore e exibe cada especialidade com seus diagnósticos
def consultar_arvore(): #Cria a função consulta
  print("\n==== ESPECIALIDADES E DIAGNÓSTICOS ====")

  if len(arvore_especialidades) == 0: #Verifica se não existem especialidades
    print("Árvore vazia.")

  else: #Executa se houver informações dentro da árvore
    for especialidade in arvore_especialidades: #Percorre todas as especialidades cadastradas
      print("\nEspecialidade:", especialidade)

      if len(arvore_especialidades[especialidade]) == 0: #Verifica se a especialidade informada tem diagnósticos
        print("  Nenhum diagnóstico cadastrado.")

      else: #Executa quando existem diagnósticos
        for diagnostico in arvore_especialidades[especialidade]: #Percorre os diagnósticos daquela especialidade
          print("  |--", diagnostico) #Exibe cada diagnóstico a baixo da especialidade correspondente

## Permite alterar o nome de uma especialidade ou de um diagnóstico na árvore
def atualizar_arvore(): #Cria a função de atualização
  print("\n==== ATUALIZAR ÁRVORE ====")
  print("1- Alterar especialidade")
  print("2- Alterar diagnóstico")

  opcao = input("Escolha uma opção: ")

  if opcao == "1": #Alterar especialidade
    antiga = ler_campo("Especialidade atual: ") #Informa a especialidade que deseja alterar

    if antiga in arvore_especialidades: #Verifica se a especialidade existe
      nova = ler_campo("Novo nome: ") #Informa o novo nome

      if nova not in arvore_especialidades: #Verifica se o novo nome ainda não esta cadastrado
        arvore_especialidades[nova] = arvore_especialidades[antiga] #Cria uma nova chave com o nome novo, transferindo os diagnósticos da especialidade antiga
        del arvore_especialidades[antiga] #Exclui a chave antiga

        print("Especialidade atualizada!")

      else: #Informa quando o nome da especialidade já existe
        print("Essa especialidade já existe.")

    else: #Informa quando a especialidade informada não existe
      print("Especialidade não encontrada.")

  elif opcao == "2": #Alterar diagnóstico
    especialidade = ler_campo("Informe a especialidade: ") #Informa a especialidade onde o diagnóstico desejado está

    if especialidade in arvore_especialidades: #Verifica se a especialidade existe
      antigo = ler_campo("Diagnóstico atual: ") #Recebe o diagnóstico no qual se deseja alterar

      if antigo in arvore_especialidades[especialidade]: #Verifica se o diagnóstico existe dentro da especialide informada
        novo = ler_campo("Novo diagnóstico: ") #Recebe o novo nome do diagnóstico

        if novo not in arvore_especialidades[especialidade]: #Verifica se o nome escolhido do diagnóstico existe na especialidade
          arvore_especialidades[especialidade][novo] = {} #Cria o diagnóstico com o nome novo
          del arvore_especialidades[especialidade][antigo] #Exclui o diagnóstico com o nome antigo

          print("Diagnóstico atualizado!")

        else: #Informa se o nome escolhido para o diagnóstico já existe
          print("Esse diagnóstico já existe.")

      else: #Informa se o diagnóstico não existe dentro daquela especialidade
        print("Diagnóstico não encontrado.")

    else: #Informa se a especialidade não existe
      print("Especialidade não encontrada.")

  else: #Informa que a opção desejada não existe
    print("Opção inválida.")

## Permite excluir uma especialidade inteira ou somente um diagnóstico
def excluir_arvore(): #Cria a função de exclusão
  print("\n==== EXCLUIR DA ÁRVORE ====")
  print("1- Excluir especialidade")
  print("2- Excluir diagnóstico")

  opcao = input("Escolha uma opção: ")

  if opcao == "1": #Excluir especialidade
    especialidade = ler_campo("Informe a especialidade: ") #Recebe o nome da especialidade desejada

    if especialidade in arvore_especialidades: #Verifica se a especialidade existe
      del arvore_especialidades[especialidade] #Exclui a especialidade

      print("Especialidade e seus diagnósticos excluídos!")

    else: #Infoma se a especalidade informada não existir
      print("Especialidade não encontrada.")

  elif opcao == "2": #Excluir diagnóstico
    especialidade = ler_campo("Informe a especialidade: ") #Recebe o nome da especialidade que ariga o diagnóstico desejado

    if especialidade in arvore_especialidades: #Verifica se a especialidade existe
      diagnostico = ler_campo("Informe o diagnóstico: ") #Recebe o nome do diagnóstico desejado

      if diagnostico in arvore_especialidades[especialidade]: #Verifica se o diagnóstico existe dentro da especialidade informada
        del arvore_especialidades[especialidade][diagnostico] #Exclui o diagnóstico

        print("Diagnóstico excluído!")

      else: #Informa se o diagnóstico não existir dentro da especialidade informada
        print("Diagnóstico não encontrado.")

    else: #Informa se a esecialidade informada não existir
      print("Especialidade não encontrada.")

  else:
    print("Opção inválida.")

## Menu responsável por acessar as operações da árvore de especialidades
def menu_arvore():
  while True:
    print("\n==== ÁRVORE DE ESPECIALIDADES ====")
    print("1- Cadastrar especialidade")
    print("2- Cadastrar diagnóstico")
    print("3- Consultar árvore")
    print("4- Atualizar especialidade/diagnóstico")
    print("5- Excluir especialidade/diagnóstico")
    print("0- Voltar")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
      adicionar_especialidade()

    elif opcao == "2":
      adicionar_diagnostico()

    elif opcao == "3":
      consultar_arvore()

    elif opcao == "4":
      atualizar_arvore()

    elif opcao == "5":
      excluir_arvore()

    elif opcao == "0":
      break

    else:
      print("Opção inválida!")

## Salva as informações de todas as estruturas no arquivo TXT
def salvar_dados(): #Cria a função de Salvamento
  with open(arquivo, "w", encoding="utf-8") as arq: #Abre o arquivo para a gravação
  #"arquivo": utiliza o nome definido no início do programa
  #w: Indica que o arquivo vai ser aberto no modo "escrita"
  #encoding="utf-8": permite trabalhar corretamente com caracteres como acentos
  #as arq: cria o nome arq para representar o arquivo dentro desse bloco.

    for paciente in lista_pacientes: #Percorre todos os pacientes cadastrados
      arq.write( #Escreve as informações no arquivo
          f"LISTA|{paciente['id']}|{paciente['nome']}|"
          f"{paciente['leito']}|{paciente['status']}|"
          f"{paciente['doenca']}\n"
      )

    for paciente in fila_triagem: #Percorre todos os paciente presentes na fila
      arq.write( #Escreve as informações no arquivo
          f"FILA|{paciente['id']}|{paciente['nome']}|"
          f"{paciente['prioridade']}\n"
      )

    for prontuario in pilha_prontuarios: #Percorre todos os prontuários
      arq.write( #Escreve as informações no arquivo
          f"PILHA|{prontuario['id']}|{prontuario['paciente']}|"
          f"{prontuario['especialidade']}\n"
      )

    for especialidade in arvore_especialidades: #Percorre todas as especialidade cadastradas
      if len(arvore_especialidades[especialidade]) == 0: #Verifica se a especialidade não possui diagnósticos
        arq.write(f"ARVORE|{especialidade}|\n") #Grava a especialidade, mesmo sem diagnósticos

      else: #Executa quando existem diagnósticos
        for diagnostico in arvore_especialidades[especialidade]: #Percorre os diagnósticos daquela especialidade
          arq.write(f"ARVORE|{especialidade}|{diagnostico}\n") #Grava a especialidade com os seus diagnósticos

  print("Dados salvos com sucesso!")

## Lê o arquivo TXT e recupera os dados nas estruturas correspondentes
def carregar_dados(): #Cria a função responsável por recuperar dados
  if not os.path.exists(arquivo): #Verifica se o arquivo informado não existe
    print("Arquivo de dados não encontrado.")

  else: #Executa quando o arquivo existe
    lista_pacientes.clear() #Limpa a lista
    fila_triagem.clear() #Limpa a fila
    pilha_prontuarios.clear() #Limpa a pilha
    arvore_especialidades.clear() #Limpa os elementos da árvore
    #Limpa para evitar que os dados sejam duplicados

    with open(arquivo, "r", encoding="utf-8") as arq: #Abre o arquivo no modo de leitura
      for linha in arq: #Percorre linha por linha do arquivo
        dados = linha.strip().split("|") #Remove espaços em branco e separa as informações com "|"

        if dados[0] == "LISTA" and len(dados) == 6: #Verifica se a linha pertence a lista de pacientes
          paciente = { #Cria um dicionário com os dados recuperados dos pacientes
              "id": dados[1],
              "nome": dados[2],
              "leito": dados[3],
              "status": dados[4],
              "doenca": dados[5]
          }

          lista_pacientes.append(paciente) #Adiciona o paciente a lista

        elif dados[0] == "FILA" and len(dados) == 4: #Verifica se a linha pertence a fila
          paciente = { #Cria um dicionário com os dados recuperados dos pacientes da fila
              "id": dados[1],
              "nome": dados[2],
              "prioridade": dados[3]
          }

          fila_triagem.append(paciente) #Adiciona o paciente ao final da fila

        elif dados[0] == "PILHA" and len(dados) == 4: #Verifica se a linha pertence a pilha
          prontuario = { #Cria um dicionário com os dados recuperados dos protuários
              "id": dados[1],
              "paciente": dados[2],
              "especialidade": dados[3]
          }

          pilha_prontuarios.append(prontuario) #Adiciona o prontuário a pilha

        elif dados[0] == "ARVORE" and len(dados) == 3: #Indentifica se a linha pertence a árvore
          especialidade = dados[1] #Recupera o nome da especialidade
          diagnostico = dados[2] #Recupera o nome do diagnóstico

          if especialidade not in arvore_especialidades: #Verifica se a especialidade ainda não existe no dicionário
            arvore_especialidades[especialidade] = {} #Cria a especialidade com um dicionário vazio

          if diagnostico != "": #Verifica se existe um diagnóstico
            arvore_especialidades[especialidade][diagnostico] = {} #Adiciona o diagnóstico dentro da especialidade

    print("Dados carregados com sucesso!")

## Menu principal responsável por acessar todas as estruturas e operações do sistema
while True:
  print("\n==== SISTEMA HOSPITALAR ====")
  print("1- Gerenciar pacientes")
  print("2- Gerenciar fila")
  print("3- Gerenciar histórico")
  print("4- Gerenciar especialidades")
  print("5- Salvar dados")
  print("6- Carregar dados")
  print("7- Sair")

  opcao = input("Escolha uma opção: ")

  if opcao == "1":
    menu_pacientes()

  elif opcao == "2":
    menu_fila()

  elif opcao == "3":
    menu_prontuarios()

  elif opcao == "4":
    menu_arvore()

  elif opcao == "5":
    salvar_dados()

  elif opcao == "6":
    carregar_dados()

  elif opcao == "7":
    print("Programa encerrado.")
    break

  else:
    print("Opção inválida!")
