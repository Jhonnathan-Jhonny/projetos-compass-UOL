# Sprint 1 - Compass UOL AWS

## Objetivos

Criar um CRUD simples utilizando HTML, CSS e JavaScript, armazenando os dados localmente no navegador com `localStorage`.  
Aplicar o padrão de projeto `Factory Method` para organizar o cadastro dos usuários, facilitando futuras expansões com novos tipos de usuários.

---

## O que foi feito

### Back-end (JavaScript)

- Cadastro de usuário com os seguintes campos:
  - Nome
  - Data de nascimento
  - Telefone
  - Email
- Deletar usuário utilizando posição do array como identificador.
- Atualizar usuário utilizando posição do array como identificador.
- Exibir todos os usuários cadastrados.

### Front-end

- Criação de formulários em HTML para cadastro, edição e exclusão de usuários.
- Estilização com CSS para melhor apresentação dos elementos na tela.
- Utilização de JavaScript para:
  - Captura e validação dos dados inseridos nos formulários.
  - Armazenamento dos dados no `localStorage`.
  - Atualização dinâmica da lista de usuários exibidos.
  - Edição e exclusão de usuários diretamente pela interface.
- Feedback visual ao usuário, com mensagens de sucesso ou erro após ações como cadastro, exclusão e atualização.

---

## Organização do Projeto

O projeto está dividido em pastas para facilitar a organização:

- `assets/css` – Estilos da aplicação.
- `assets/images` – Imagens e ícones utilizados.
- `assets/js` – Lógica JavaScript, com separação por responsabilidades:
  - `arquivo.js` – Script principal.
  - `factory/userFactory.js` – Implementação do padrão Factory para criação de usuários.
  
---

## Quadro de Planejamento (Trello)

Acompanhe o progresso das tarefas através do quadro do Trello:  
🔗 [Planejamento da Sprint 1 - Trello](https://trello.com/invite/b/682cbb77221d5468dafc2769/ATTI73c9aad954a50842f8a730a7209ede858CB2884F/planejamento-do-desafio-da-sprint-1)

---

## Autor

Jhonnathan Jhonny Rufino Rodrigues
