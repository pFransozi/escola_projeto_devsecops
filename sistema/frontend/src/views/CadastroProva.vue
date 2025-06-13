<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Provas</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog">Nova Prova</v-btn>
    </v-toolbar>

    <v-data-table
      :headers="headers"
      :items="provas"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
      loading-text="Carregando provas..."
    >
      <!-- Slot para formatar a coluna 'data' -->
      <template #item.data="{ item }">
        {{ formatDate(item.data) }}
      </template>

      <!-- Slots para exibir textos enriquecidos -->
      <template #item.nome_professor="{ item }">
        {{ item.nome_professor }}
      </template>
      <template #item.aula_descricao="{ item }">
        {{ item.aula_descricao }}
      </template>
      <template #item.turma_descricao="{ item }">
        {{ item.turma_descricao }}
      </template>

      <!-- Ações -->
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
            {{ editedIndex === -1 ? 'Nova Prova' : 'Editar Prova' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field v-model="editedItem.descricao" label="Descrição da Prova" required />
            <v-text-field
              v-model="editedItem.data"
              label="Data da Prova"
              placeholder="dd/mm/aaaa"
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
              v-model="editedItem.aula_id"
              :items="aulasOptions"
              item-title="label"
              item-value="value"
              label="Aula"
              required
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn text @click="closeDialog">Cancelar</v-btn>
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
const provas = ref([])
const professoresOptions = ref([])
const aulasOptions = ref([])
const editedIndex = ref(-1)
const editedItem = ref({ id: null, descricao: '', data: '', professor_id: null, aula_id: null })

// Cabeçalhos no padrão Vuetify 3 Labs
const headers = [
  { title: 'ID',             key: 'id',               align: 'start', width: '80px' },
  { title: 'Descrição',      key: 'descricao',        align: 'start'               },
  { title: 'Data',           key: 'data',             align: 'center'              },
  { title: 'Professor',      key: 'nome_professor',   align: 'start'               },
  { title: 'Aula',           key: 'aula_descricao',   align: 'start'               },
  { title: 'Turma',          key: 'turma_descricao',  align: 'start'               },
  { title: 'Ações',          key: 'actions',          sortable: false, align: 'center' }
]

function formatDate(value) {
  if (!value) return ''
  const dt = new Date(value)
  const d = String(dt.getUTCDate()).padStart(2, '0')
  const m = String(dt.getUTCMonth() + 1).padStart(2, '0')
  const y = dt.getUTCFullYear()
  return `${d}/${m}/${y}`
}

function formatDateReverse(dateStr) {
  const [d, m, y] = dateStr.split('/')
  return `${y}-${m}-${d}`
}

async function fetchProvas() {
  loading.value = true
  try {
    const res = await api.get('/api/prova')
    provas.value = res.data.data
  } catch {
    window.dispatchEvent(new CustomEvent('http-error', { detail: 'Erro ao carregar provas.' }))
  } finally {
    loading.value = false
  }
}

async function fetchProfessores() {
  try {
    const res = await api.get('/api/professor')
    professoresOptions.value = res.data.data.map(p => ({ label: p.nome_usuario, value: p.id }))
  } catch {
    console.error('Erro ao carregar professores')
  }
}

async function fetchAulas() {
  try {
    const res = await api.get('/api/aula')
    aulasOptions.value = res.data.data.map(a => ({ label: `${a.descricao} - Turma: ${a.turma_descricao}`, value: a.id }))
  } catch {
    console.error('Erro ao carregar aulas')
  }
}

function openDialog(item) {
  if (item) {
    editedIndex.value = provas.value.findIndex(p => p.id === item.id)
    const clone = { ...item }
    if (clone.data) clone.data = formatDate(clone.data)
    editedItem.value = clone
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, descricao: '', data: '', professor_id: null, aula_id: null }
  }
  dialog.value = true
}

function closeDialog() {
  dialog.value = false
}

async function save() {
  const payload = { ...editedItem.value, data: formatDateReverse(editedItem.value.data) }
  try {
    if (editedIndex.value > -1) {
      await api.put(`/api/prova/${payload.id}`, payload)
    } else {
      await api.post('/api/prova', payload)
    }
    await fetchProvas()
    closeDialog()
    window.dispatchEvent(new CustomEvent('http-success', { detail: 'Prova salva com sucesso!' }))
  } catch {
    window.dispatchEvent(new CustomEvent('http-error', { detail: 'Erro ao salvar prova.' }))
  }
}

function confirmDelete(item) {
  if (confirm(`Deseja remover a prova "${item.descricao}"?`)) {
    api.delete(`/api/prova/${item.id}`)
      .then(() => {
        fetchProvas()
        window.dispatchEvent(new CustomEvent('http-success', { detail: 'Prova removida com sucesso!' }))
      })
      .catch(() => {
        window.dispatchEvent(new CustomEvent('http-error', { detail: 'Erro ao deletar prova.' }))
      })
  }
}

onMounted(() => {
  fetchProfessores()
  fetchAulas()
  fetchProvas()
})
</script>
