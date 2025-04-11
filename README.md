# escola_projeto_devsecops

1.	Descrição Geral do Sistema
O sistema proposto é uma aplicação web voltada para gestão escolar, com funcionalidades para facilitar o gerenciamento acadêmico e administrativo de uma instituição de ensino. Seu objetivo principal é otimizar processos relacionados ao cadastro e controle de alunos, professores, disciplinas, turmas, atividades escolares, avaliações e divulgação de informações, oferecendo maior eficiência e organização.

2.	Descrição dos Usuários
•	Administrador: Controla o sistema integralmente, gerenciando cadastros e conteúdo.
•	Professor: Responsável pela criação de atividades, lançamento e consulta de notas e acompanhamento do desempenho acadêmico dos alunos.
•	Aluno: Usuário que acessa suas informações acadêmicas, atividades atribuídas, notas e avisos escolares.

3.	Requisitos Funcionais

| Código | Nome                             | Descrição                                                                 | Prioridade |
|--------|----------------------------------|---------------------------------------------------------------------------|------------|
| RF01   | Gerenciar Alunos                 | Permitir cadastrar, editar e remover alunos.                              | Alta       |
| RF02   | Cadastro de Professores          | Permite cadastrar, editar ou excluir professores.                         | Alta       |
| RF03   | Cadastro de Disciplinas          | Permite criar, editar e excluir disciplinas no sistema                    | Alta       |
| RF04   | Gestão de Turmas                 | Gerenciar turmas, incluindo cadastro e edição                             | Alta       |
| RF05   | Cadastro de Notícias             | Permite cadastrar, editar e excluir notícias escolares                    | Média      |
| RF06   | Lançamento de Notas              | Permite o professor lançar notas de atividades no sistema                 | Alta       |
| RF07   | Cadastro de Atividades           | Criar, editar e excluir atividades                                        | Alta       |
| RF08   | Visualizar Notas                 | Permitir aos alunos consultar suas notas                                  | Alta       |
| RF09   | Login de Usuários                | Realizar autenticação segura de usuários                                  | Alta       |
| RF10   | Painel Administrativo            | Área para gestão de todo o sistema                                        | Alta       |
| RF11   | Gestão de Perfil                 | Usuários podem atualizar seus dados pessoais                              | Média      |
| RF12   | Recuperação de Senha             | Permite recuperação segura da senha de usuários                           | Alta       |
| RF13   | Emissão de Relatórios            | Gerar relatórios acadêmicos e administrativos detalhados                  | Média      |
| RF14   | Cadastro de Atividades Escolares | Permite aos professores criar, editar e remover atividades                | Alta       |
| RF15   | Histórico Acadêmico              | Consultar histórico acadêmico completo dos alunos                         | Média      |
| RF16   | Controle de Acessos              | Definir diferentes níveis de acesso com permissões específicas            | Alta       |
| RF17   | Notificações do Sistema          | Enviar alertas automáticos sobre prazos e avisos                          | Média      |
| RF18   | Recuperação de Senha Alternativa | Facilitar recuperação segura de senhas                                    | Alta       |
| RF19   | Gestão de Perfil Alternativa     | Permitir que usuários atualizem dados pessoais                            | Média      |
| RF20   | Alertas de Estoque               | Notificar administradores sobre materiais escolares necessários           | Média      |
| RF21   | Acompanhamento de Presença       | Registrar e acompanhar frequência dos alunos                              | Média      |
| RF22   | Exportação de Dados              | Exportar informações do sistema em formatos diversos                      | Média      |
| RF23   | Envio de Notificações            | Enviar notificações automáticas sobre eventos ou atualizações             | Média      |
| RF24   | Pesquisa Interna                 | Permitir pesquisa rápida e eficiente de informações dentro do sistema     | Média      |


4.	Requisitos Não-Funcionais

| Código | Nome                    | Categoria      | Descrição                                                                                 | Prioridade |
|--------|-------------------------|----------------|-------------------------------------------------------------------------------------------|------------|
| RNF01  | Backup Regular          | Confiabilidade | Realizar backups periódicos do banco de dados                                             | Alta       |
| RNF02  | Segurança dos Dados     | Segurança      | Garantir a proteção e privacidade dos dados armazenados                                   | Alta       |
| RNF03  | Usabilidade Geral       | Usabilidade    | Interface intuitiva e acessível para todos os usuários                                    | Alta       |
| RNF04  | Desempenho              | Eficiência     | Tempo rápido de resposta nas interações                                                   | Alta       |
| RNF05  | Compatibilidade         | Portabilidade  | Compatível com os principais navegadores e dispositivos móveis                            | Média      |
| RNF06  | Disponibilidade         | Confiabilidade | Disponibilidade operacional mínima de 99,9%                                               | Alta       |
| RNF07  | Escalabilidade          | Eficiência     | Suportar aumento no número de usuários e volume de dados sem perda de desempenho          | Média      |
| RNF08  | Usabilidade Inclusiva   | Usabilidade    | Interface intuitiva e acessível para diferentes tipos de usuários                         | Alta       |
| RNF09  | Manutenibilidade        | Manutenção     | Código estruturado e documentado, facilitando futuras atualizações                        | Média      |
