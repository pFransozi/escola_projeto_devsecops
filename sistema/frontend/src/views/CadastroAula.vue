<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Aulas</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Nova Aula</v-btn>
    </v-toolbar>

    <v-data-table
      :headers="headers"
      :items="aulas"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
      loading-text="Carregando aulas..."
    >
      <!-- Exibe nome do professor -->
      <template #item.nome_professor="{ item }">
        {{ item.nome_professor }}
      </template>
      <!-- Exibe descrição da turma -->
      <template #item.turma_descricao="{ item }">
        {{ item.turma_descricao }}
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
            {{ editedIndex === -1 ? 'Nova Aula' : 'Editar Aula' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedItem.descricao"
              label="Descrição da Aula"
              required
            />
            <v-select
              v-model="editedItem.professor_id"
              :items="professoresOptions"
              item-title="label"
              item-value="value"
              label="Professor"
              required
            />
            <v-select
              v-model="editedItem.turma_id"
              :items="turmasOptions"
              item-title="label"
              item-value="value"
              label="Turma"
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
const aulas = ref([])
const professoresOptions = ref([])
const turmasOptions = ref([])
const editedIndex = ref(-1)
const editedItem = ref({ id: null, descricao: '', professor_id: null, turma_id: null })

// Cabeçalhos no padrão Vuetify 3 (Labs)
const headers = [
  { title: 'ID',         key: 'id',              align: 'start', width: '80px' },
  { title: 'Descrição',  key: 'descricao',       align: 'start' },
  { title: 'Professor',   key: 'nome_professor',  align: 'start' },
  { title: 'Turma',      key: 'turma_descricao', align: 'start' },
  { title: 'Ações',      key: 'actions',         sortable: false, align: 'center' }
]

async function fetchProfessoresOptions() {
  try {
    const res = await api.get('/api/professor')
    professoresOptions.value = res.data.data.map(p => ({ label: p.nome_usuario, value: p.id }))
  } catch (err) {
    console.error('Erro ao carregar professores:', err)
  }
}

async function fetchTurmasOptions() {
  try {
    const res = await api.get('/api/turma')
    turmasOptions.value = res.data.data.map(t => ({ label: `${t.descricao} (${t.sala})`, value: t.id }))
  } catch (err) {
    console.error('Erro ao carregar turmas:', err)
  }
}

async function fetchAulas() {
  loading.value = true
  try {
    const res = await api.get('/api/aula')
    aulas.value = res.data.data
  } catch (err) {
    console.error('Erro ao carregar aulas:', err)
  } finally {
    loading.value = false
  }
}

function openDialog(item) {
  if (item) {
    editedIndex.value = aulas.value.findIndex(a => a.id === item.id)
    editedItem.value = { ...item }
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, descricao: '', professor_id: null, turma_id: null }
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
      await api.put(`/api/aula/${payload.id}`, payload)
    } else {
      await api.post('/api/aula', payload)
    }
    await fetchAulas()
    closeDialog()
  } catch (err) {
    alert(err.response?.data?.message || 'Erro ao salvar')
  }
}

function confirmDelete(item) {
  if (confirm(`Deseja remover a aula "${item.descricao}"?`)) {
    api.delete(`/api/aula/${item.id}`)
      .then(fetchAulas)
      .catch(err => alert(err.response?.data?.message || 'Erro ao deletar'))
  }
}

onMounted(async () => {
  await fetchProfessoresOptions()
  await fetchTurmasOptions()
  await fetchAulas()
})
</script>
