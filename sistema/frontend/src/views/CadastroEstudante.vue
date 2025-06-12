<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Estudantes</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Novo Estudante</v-btn>
    </v-toolbar>

    <v-data-table
      :columns="columns"
      :items="estudantes"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
      loading-text="Carregando estudantes..."
    >
      <!-- Exibe nome do estudante -->
      <template #item.nome_estudante="{ item }">
        {{ item.nome_estudante }}
      </template>
      <!-- Ações de editar e deletar -->
      <template #item.actions="{ item }">
        <v-icon small class="mr-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon small @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <!-- Dialog de criação/edição -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h6">
            {{ editedIndex === -1 ? 'Novo Estudante' : 'Editar Estudante' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-row>
              <v-col cols="6">
                <v-select
                  v-model="editedItem.id"
                  :items="usuariosAluno"
                  item-title="label"
                  item-value="value"
                  label="Estudante"
                  required
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.responsavel_1"
                  label="Responsável 1"
                  required
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.fone_resp_1"
                  label="Fone Resp. 1"
                  required
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.responsavel_2"
                  label="Responsável 2"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.fone_resp_2"
                  label="Fone Resp. 2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.comentarios"
                  label="Comentários"
                  rows="3"
                />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="closeDialog()">Cancelar</v-btn>
          <v-btn color="primary" @click="save">Salvar</v-btn>
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
const estudantes = ref([])
const usuariosAluno = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  responsavel_1: '',
  fone_resp_1: '',
  responsavel_2: '',
  fone_resp_2: '',
  comentarios: ''
})

// =======================================
// Cabeçalho da tabela
// =======================================
const columns = [
  { text: 'ID',             value: 'id',              align: 'start', width: '80px' },
  { text: 'Estudante',      value: 'nome_estudante',  align: 'start'            },
  { text: 'Responsável 1',  value: 'responsavel_1',   align: 'start'            },
  { text: 'Fone Resp. 1',   value: 'fone_resp_1',     align: 'start'            },
  { text: 'Responsável 2',  value: 'responsavel_2',   align: 'start'            },
  { text: 'Fone Resp. 2',   value: 'fone_resp_2',     align: 'start'            },
  { text: 'Comentários',    value: 'comentarios',     align: 'start'            },
  { text: 'Ações',          value: 'actions', sortable: false, align: 'center' }
]

async function fetchEstudantes() {
  loading.value = true
  try {
    const res = await api.get('/api/estudante')
    estudantes.value = res.data.data
  } catch (err) {
    console.error('Erro ao carregar estudantes:', err)
  } finally {
    loading.value = false
  }
}

async function fetchUsuariosAluno() {
  try {
    const res = await api.get('/api/usuario')
    usuariosAluno.value = res.data.data
      .filter(u => u.tipo === 'aluno')
      .map(u => ({ label: `${u.nome} ${u.ultimo_nome}`, value: u.id }))
  } catch (err) {
    console.error('Erro ao carregar usuários:', err)
  }
}

function openDialog(item) {
  if (item) {
    editedIndex.value = estudantes.value.findIndex(e => e.id === item.id)
    editedItem.value = { ...item }
  } else {
    editedIndex.value = -1
    editedItem.value = {
      id: null,
      responsavel_1: '',
      fone_resp_1: '',
      responsavel_2: '',
      fone_resp_2: '',
      comentarios: ''
    }
  }
  dialog.value = true
}

function closeDialog() {
  dialog.value = false
}

async function save() {
  const payload = { ...editedItem.value }
  try {
    if (editedIndex.value > -1) {
      await api.put(`/api/estudante/${payload.id}`, payload)
    } else {
      await api.post('/api/estudante', payload)
    }
    await fetchEstudantes()
    closeDialog()
  } catch (err) {
    alert(err.response?.data?.message || 'Erro ao salvar')
  }
}

function confirmDelete(item) {
  if (confirm(`Deseja remover o estudante ${item.nome_estudante}?`)) {
    api.delete(`/api/estudante/${item.id}`)
      .then(fetchEstudantes)
      .catch(err => alert(err.response?.data?.message || 'Erro ao deletar'))
  }
}

onMounted(async () => {
  await fetchUsuariosAluno()
  await fetchEstudantes()
})
</script>
