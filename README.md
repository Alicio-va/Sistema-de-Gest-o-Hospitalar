# Sistema de Gestão Hospitalar

Programa de terminal em Python que simula quatro rotinas de um hospital: pacientes internados, fila de triagem, histórico de prontuários e organização de especialidades médicas com seus diagnósticos. Cada rotina usa uma estrutura de dados diferente, escolhida pela forma como os dados são acessados naquela situação.

## Requisitos

- Python 3.6 ou superior (o código usa f-strings).
- Nenhuma instalação adicional. O programa usa apenas `collections` e `os`, que já vêm com o Python.

## Como executar

1. Salve o código em um arquivo, por exemplo `sistema_hospitalar.py`.
2. Abra um terminal na pasta onde o arquivo está.
3. Execute:

```bash
python sistema_hospitalar.py
```

Em Linux e macOS, se `python` apontar para a versão 2, use `python3`:

```bash
python3 sistema_hospitalar.py
```

O menu principal aparece assim:

```
==== SISTEMA HOSPITALAR ====
1- Gerenciar pacientes
2- Gerenciar fila
3- Gerenciar histórico
4- Gerenciar especialidades
5- Salvar dados
6- Carregar dados
7- Sair
```

A navegação é feita digitando o número da opção e pressionando Enter. Cada submenu tem a opção `0` para voltar ao menu principal.

### Salvar e carregar dados

Os dados ficam em memória enquanto o programa roda. Para guardá-los, use a opção 5, que grava o arquivo `dados_sistema.txt` na pasta de execução. A opção 6 lê esse arquivo e restaura as quatro estruturas.

Três comportamentos a conhecer:

- O programa não carrega o arquivo sozinho ao iniciar. Na segunda execução, escolha a opção 6 antes de qualquer outra coisa.
- A opção 7 encerra sem salvar. Quem não usar a opção 5 antes perde as alterações.
- A opção 6 apaga o que está em memória antes de ler o arquivo. Cadastros feitos e não salvos são descartados.

### Formato do arquivo

Cada linha começa com o tipo do registro e separa os campos por `|`:

```
LISTA|id|nome|leito|status|doenca
FILA|id|nome|prioridade
PILHA|id_prontuario|id_paciente|especialidade
ARVORE|especialidade|diagnostico
```

Por isso a função `ler_campo` recusa campos vazios e o caractere `|`: um `|` digitado pelo usuário quebraria a leitura da linha. Uma especialidade sem diagnósticos é gravada como `ARVORE|especialidade|`, com o último campo vazio.

## Módulos do sistema

| Menu | Estrutura | Uso no hospital | Regra de acesso |
|---|---|---|---|
| Gerenciar pacientes | Lista | Cadastro de internados | Busca por ID |
| Gerenciar fila | Fila (`deque`) | Triagem | FIFO |
| Gerenciar histórico | Pilha (lista) | Acessos a prontuários | LIFO |
| Gerenciar especialidades | Árvore (dicionários aninhados) | Especialidades e diagnósticos | Navegação por nível |

## Justificativa técnica das estruturas

### Lista: pacientes internados

Variável: `lista_pacientes`. Cada paciente é um dicionário com `id`, `nome`, `leito`, `status` e `doenca`.

O cadastro de internados precisa de operações em qualquer posição: consultar um paciente pelo ID, alterar um campo, excluir quem recebeu alta e listar todos. Nenhuma ordem de entrada ou saída é imposta. A lista do Python serve a esse caso porque guarda os registros em sequência, permite percorrê-los com um laço e remover um elemento pelo índice (`pop(i)`).

A busca por ID é linear, com custo O(n). Para o volume de um trabalho acadêmico ou de uma enfermaria pequena isso não pesa. Num hospital com milhares de internados simultâneos, o ID deveria ser a chave de um dicionário, o que traria a busca para O(1) em média. A lista foi mantida porque o enunciado pede a estrutura e porque a listagem completa, que é a operação mais frequente num painel de internados, já é um percurso sequencial.

A verificação de ID duplicado em `cadastrar_paciente` também é um percurso completo da lista.

### Fila: triagem

Variável: `fila_triagem`, um `collections.deque`. Cada item guarda `id`, `nome` e `prioridade`.

A triagem funciona por ordem de chegada: quem entra primeiro é atendido primeiro (FIFO). `adicionar_fila` insere no fim com `append`, e `atender_paciente` retira do início com `popleft`. A atualização de nome ou prioridade altera o dicionário no lugar, então o paciente mantém a posição.

A escolha do `deque` em vez de uma lista comum vem do custo da retirada no início. Em uma lista, `pop(0)` desloca todos os elementos restantes e custa O(n). No `deque`, `append` e `popleft` custam O(1). Numa fila que só cresce pelo fim e só diminui pelo início, essa é a diferença que importa.

Limitação conhecida: o campo `prioridade` é texto livre e não altera a ordem de atendimento. A fila é estritamente FIFO. Um sistema que priorizasse casos graves exigiria uma fila de prioridade (por exemplo, com o módulo `heapq`).

### Pilha: histórico de prontuários

Variável: `pilha_prontuarios`, uma lista usada como pilha. Cada item guarda `id`, `paciente` e `especialidade`.

O histórico de acessos tem uma regra de uso própria: o que interessa primeiro é o acesso mais recente. A pilha segue a regra LIFO (o último a entrar é o primeiro a sair), e a implementação usa as operações que a lista do Python já faz em O(1) no fim:

- `append` empilha um novo acesso (`adicionar_prontuario`).
- `pilha_prontuarios[-1]` lê o topo sem remover (`consultar_prontuario`).
- `pop()` desempilha o topo (`remover_prontuario`).
- Um percurso do último índice ao primeiro mostra o histórico do mais novo ao mais antigo (`listar_prontuarios`).

A atualização (`atualizar_prontuario`) só alcança o topo. Isso é intencional: numa pilha, apenas o elemento do topo é acessível, e corrigir um registro mais antigo exigiria desempilhar os que estão acima dele.

### Árvore: especialidades e diagnósticos

Variável: `arvore_especialidades`, um dicionário de dicionários.

A relação entre especialidade e diagnóstico é hierárquica: um diagnóstico pertence a uma especialidade, e uma especialidade agrupa vários diagnósticos. Isso forma uma árvore com três níveis:

```
(raiz: o dicionário arvore_especialidades)
 |-- Cardiologia
 |    |-- Arritmia
 |    |-- Insuficiência cardíaca
 |-- Ortopedia
      |-- Fratura
```

A raiz é o próprio dicionário, as chaves do primeiro nível são as especialidades e as chaves do segundo nível são os diagnósticos. Cada diagnóstico guarda um dicionário vazio, que ficaria disponível caso a árvore ganhasse um terceiro nível, como medicamentos ou procedimentos.

Usar dicionários em vez de uma classe de nó com ponteiros tem duas vantagens aqui. A busca de um nó por nome é O(1) em média em cada nível, e o código fica curto: `especialidade in arvore_especialidades` verifica a existência, e `del` remove um ramo inteiro. Excluir uma especialidade apaga seus diagnósticos juntos, o que reproduz a remoção de uma subárvore.

A renomeação (`atualizar_arvore`) cria a chave nova apontando para o mesmo conteúdo e apaga a antiga. No caso de uma especialidade, os diagnósticos são preservados porque o dicionário interno é reaproveitado.

A profundidade fixa em dois níveis abaixo da raiz é uma simplificação. Uma árvore genérica, com nós de profundidade arbitrária e percurso recursivo, seria necessária se o sistema precisasse, por exemplo, de subespecialidades.

## Resumo das operações por estrutura

| Estrutura | Inserir | Consultar | Atualizar | Remover |
|---|---|---|---|---|
| Lista | `append` no fim | Busca por ID, O(n) | Altera o dicionário encontrado | `pop(i)` pelo índice |
| Fila | `append` no fim, O(1) | Percorre do início ao fim | Altera o dicionário sem mudar a posição | `popleft`, O(1) |
| Pilha | `append` no topo, O(1) | `[-1]`, O(1) | Somente o topo | `pop()`, O(1) |
| Árvore | Nova chave no dicionário | `in` e percurso dos níveis | Renomeia chave | `del` da chave e do ramo |

## Limitações

- Os dados são pessoais e de saúde, e o arquivo `dados_sistema.txt` é texto simples, sem criptografia nem controle de acesso. O sistema serve a fins didáticos e não deve guardar dados reais de pacientes.
- A consulta, a atualização e a exclusão de pacientes usam `input` direto, sem a validação de `ler_campo`. Nessas telas, um ID vazio apenas resulta em "Paciente não encontrado".
- IDs de fila e de prontuário não são verificados contra duplicidade. Só o cadastro de pacientes faz essa checagem.
- Todos os campos são armazenados como texto, inclusive o número do leito.
