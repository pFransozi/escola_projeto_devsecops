<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Turmas</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Nova Turma</v-btn>
    </v-toolbar>

    <v-data-table
      :columns="columns"
      :items="turmas"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
      loading-text="Carregando turmas..."
    >
      <!-- Ações de editar e deletar -->
      <template #item.actions="{ item }">
        <v-icon small class="mr-2" @click="openDialog(item)">mdi-pencil</v-icon>
        <v-icon small @click="confirmDelete(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <!-- Dialog de criação/edição -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h6">
            {{ editedIndex === -1 ? 'Nova Turma' : 'Editar Turma' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedItem.descricao"
              label="Descrição da Turma"
              required
            />
            <v-text-field
              v-model="editedItem.sala"
              label="Sala"
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
const turmas = ref([])
const editedIndex = ref(-1)
const editedItem = ref({ id: null, descricao: '', sala: '' })

// =======================================
// Cabeçalho da tabela
// =======================================
const columns = [
  { text: 'ID',         value: 'id',       align: 'start', width: '80px' },
  { text: 'Descrição',  value: 'descricao', align: 'start'            },
  { text: 'Sala',       value: 'sala',      align: 'start'            },
  { text: 'Ações',      value: 'actions',   sortable: false, align: 'center' }
]

async function fetchTurmas() {
  loading.value = true
  try {
    const res = await api.get('/api/turma')
    turmas.value = res.data.data
  } catch (err) {
    console.error('Erro ao carregar turmas:', err)
  } finally {
    loading.value = false
  }
}

function openDialog(item) {
  if (item) {
    editedIndex.value = turmas.value.findIndex(t => t.id === item.id)
    editedItem.value = { ...item }
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, descricao: '', sala: '' }
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
      await api.put(`/api/turma/${payload.id}`, payload)
    } else {
      await api.post('/api/turma', payload)
    }
    await fetchTurmas()
    closeDialog()
  } catch (err) {
    alert(err.response?.data?.message || 'Erro ao salvar')
  }
}

function confirmDelete(item) {
  if (confirm(`Deseja remover a turma "${item.descricao}"?`)) {
    api.delete(`/api/turma/${item.id}`)
      .then(fetchTurmas)
      .catch(err => alert(err.response?.data?.message || 'Erro ao deletar'))
  }
}

onMounted(fetchTurmas)
</script>
