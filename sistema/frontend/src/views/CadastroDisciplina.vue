<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Disciplinas</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Nova Disciplina</v-btn>
    </v-toolbar>

    <v-data-table
      :columns="columns"
      :items="disciplinas"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
      loading-text="Carregando disciplinas..."
    >
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
            {{ editedIndex === -1 ? 'Nova Disciplina' : 'Editar Disciplina' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedItem.descricao"
              label="Nome da Disciplina"
              required
            />
            <v-textarea
              v-model="editedItem.ementa"
              label="Ementa da Disciplina"
              rows="4"
              auto-grow
              required
            />
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
const disciplinas = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  descricao: '',
  ementa: ''
})

// =======================================
// Cabeçalho da tabela
// =======================================
const columns = [
  { text: 'ID',         value: 'id',       align: 'start', width: '80px' },
  { text: 'Descrição',  value: 'descricao', align: 'start'             },
  { text: 'Ementa',     value: 'ementa',    align: 'start'             },
  { text: 'Ações',      value: 'actions',   sortable: false, align: 'center' }
]

function fetchDisciplinas() {
  loading.value = true
  api.get('/api/disciplina')
    .then(response => {
      disciplinas.value = response.data.data
    })
    .catch(err => {
      console.error('Erro ao carregar disciplinas:', err)
    })
    .finally(() => {
      loading.value = false
    })
}

function openDialog(item) {
  if (item) {
    editedIndex.value = disciplinas.value.findIndex(d => d.id === item.id)
    editedItem.value = { ...item }
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, descricao: '', ementa: '' }
  }
  dialog.value = true
}

function closeDialog() {
  dialog.value = false
}

function save() {
  const payload = { ...editedItem.value }
  let request
  if (editedIndex.value > -1) {
    request = api.put(`/api/disciplina/${payload.id}`, payload)
  } else {
    request = api.post('/api/disciplina', payload)
  }
  request
    .then(() => {
      fetchDisciplinas()
      closeDialog()
    })
    .catch(err => {
      alert(err.response?.data?.message || 'Erro ao salvar')
    })
}

function confirmDelete(item) {
  if (confirm(`Deseja remover a disciplina "${item.descricao}"?`)) {
    api.delete(`/api/disciplina/${item.id}`)
      .then(fetchDisciplinas)
      .catch(err => alert(err.response?.data?.message || 'Erro ao deletar'))
  }
}

onMounted(fetchDisciplinas)
</script>
