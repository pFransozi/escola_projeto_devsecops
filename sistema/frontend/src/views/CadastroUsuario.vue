<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Usuários</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Novo Usuário</v-btn>
    </v-toolbar>

    <v-data-table :headers="headers" :items="usuarios" :items-per-page="10" class="elevation-1" :loading="loading"
      loading-text="Carregando usuários...">
      <template #item.actions="{ item }">
        <v-icon small class="mr-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon small @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <!-- Dialog de criação/edição -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h6">{{ editedIndex === -1 ? 'Novo Usuário' : 'Editar Usuário' }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-row>
              <v-col cols="6">
                <v-text-field v-model="editedItem.nome" label="Nome" required />
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="editedItem.ultimo_nome" label="Último Nome" required />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field v-model="editedItem.usuario" label="Login" required />
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="editedItem.senha" label="Senha" type="password"
                  :rules="editedIndex === -1 ? [v => !!v || 'Senha é obrigatória'] : []" />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field v-model="editedItem.email" label="E-mail" />
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="editedItem.data_nascimento" label="Data de Nascimento"
                  placeholder="dd/mm/aaaa" />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-select v-model="editedItem.sexo" :items="[
                  { text: 'Masculino', value: 'M' },
                  { text: 'Feminino', value: 'F' }
                ]" item-title="text" item-value="value" label="Sexo" required />
              </v-col>
              <v-col cols="4">
                <v-text-field v-model="editedItem.cpf" label="CPF" />
              </v-col>
              <v-col cols="4">
                <v-text-field v-model="editedItem.endereco" label="Endereço" />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-select v-model="editedItem.tipo" :items="tipos" label="Tipo" required />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="closeDialog()">Cancelar</v-btn>
          <v-btn color="primary" @click="save()">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../utils/api'

const dialog = ref(false)
const loading = ref(false)
const dateMenu = ref(false)
const tipos = ['secretario', 'professor', 'aluno']
const usuarios = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  nome: '',
  ultimo_nome: '',
  usuario: '',
  senha: '',
  email: '',
  data_nascimento: '',
  sexo: '',
  cpf: '',
  endereco: '',
  tipo: ''
})

const headers = [
  { text: 'ID', value: 'id' },
  { text: 'Nome', value: 'nome' },
  { text: 'Usuário', value: 'usuario' },
  { text: 'E-mail', value: 'email' },
  { text: 'Tipo', value: 'tipo' },
  { text: 'Ações', value: 'actions', sortable: false }
]

function fetchUsers() {
  loading.value = true
  api
    .get('/api/usuario')
    .then(response => {
      usuarios.value = response.data.data
    })
    .catch(console.error)
    .finally(() => (loading.value = false))
}

function openDialog(item) {
  dateMenu.value = false;

  if (item) {
    editedIndex.value = usuarios.value.indexOf(item);

    // 1) Clona o objeto para não mexer no original
    const user = { ...item };

    // 2) Se existir campo data_nascimento, formata
    if (user.data_nascimento) {
      // cria um Date válido a partir da string
      const dt = new Date(user.data_nascimento);
      // extrai dia, mês e ano em UTC
      const d = String(dt.getUTCDate()).padStart(2, "0");
      const m = String(dt.getUTCMonth() + 1).padStart(2, "0");
      const y = dt.getUTCFullYear();
      user.data_nascimento = `${d}/${m}/${y}`;
    }

    // 3) Preenche o editedItem com o objeto formatado
    editedItem.value = user;
  } else {
    editedIndex.value = -1;
    editedItem.value = {
      id: null,
      nome: '',
      ultimo_nome: '',
      usuario: '',
      senha: '',
      email: '',
      data_nascimento: '',
      sexo: '',
      cpf: '',
      endereco: '',
      tipo: ''
    };
  }

  dialog.value = true;
}


function closeDialog() {
  dialog.value = false
  dateMenu.value = false
}

function formatarDataParaEnvio(data) {
  if (!data) return null;
  const [dia, mes, ano] = data.split('/');
  return `${ano}-${mes}-${dia}`;
}

function save() {
  const payload = { ...editedItem.value };
  payload.data_nascimento = formatarDataParaEnvio(payload.data_nascimento)
  let request
  if (editedIndex.value > -1) {
    request = api.put(
      `/api/usuario/${payload.id}`,
      payload
    )
  } else {
    request = api.post(
      '/api/usuario',
      payload
    )
  }
  request
    .then(() => {
      fetchUsers()
      closeDialog()
    })
    .catch(err => {
      alert(err.response.data.message || 'Erro ao salvar')
    })
}

function confirmDelete(item) {
  if (confirm(`Deseja remover o usuário ${item.nome}?`)) {
    api
      .delete(`/api/usuario/${item.id}`)
      .then(fetchUsers)
      .catch(err => alert(err.response.data.message || 'Erro ao deletar'))
  }
}

onMounted(fetchUsers)
</script>