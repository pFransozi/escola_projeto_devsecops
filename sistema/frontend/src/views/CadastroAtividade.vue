<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Atividades</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog">Nova Atividade</v-btn>
    </v-toolbar>

    <v-data-table :columns="columns" :items="atividades" :items-per-page="10" class="elevation-1" :loading="loading"
      loading-text="Carregando atividades...">
      <!-- Formatação customizada da coluna 'Data' -->
      <template #item.data="{ item }">
        {{ formatDate(item.data) }}
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
            {{ editedIndex === -1 ? 'Nova Atividade' : 'Editar Atividade' }}
          </span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form">
            <v-row>
              <v-col cols="8">
                <v-text-field v-model="editedItem.descricao" label="Descrição da Atividade" required />
              </v-col>
              <v-col cols="4">
                <v-text-field v-model="editedItem.custo" label="Custo" type="number" required />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field v-model="editedItem.data" label="Data da Atividade" placeholder="dd/mm/aaaa" />
              </v-col>
            </v-row>
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
const atividades = ref([])
const editedIndex = ref(-1)
const editedItem = ref({ id: null, descricao: '', custo: null, data: '' })

// Vuetify 3 usa `columns` em vez de `headers`
const columns = [
  { title: 'ID', key: 'id', fixed: 'start', width: '80px' },
  { title: 'Descrição', key: 'descricao' },
  { title: 'Custo', key: 'custo' },
  { title: 'Data', key: 'data' },
  { title: 'Ações', key: 'actions', sortable: false }
]

function formatDate(value) {
  if (!value) return ''
  const dt = new Date(value)
  const d = String(dt.getUTCDate()).padStart(2, '0')
  const m = String(dt.getUTCMonth() + 1).padStart(2, '0')
  const y = dt.getFullYear()
  return `${d}/${m}/${y}`
}

function formatDateReverse(dateStr) {
  const [d, m, y] = dateStr.split('/')
  return `${y}-${m}-${d}`
}

async function fetchAtividades() {
  loading.value = true
  try {
    const res = await api.get('/api/atividade')
    atividades.value = res.data.data
  } catch {
    window.dispatchEvent(
      new CustomEvent('http-error', { detail: 'Erro ao carregar atividades.' })
    )
  } finally {
    loading.value = false
  }
}

function openDialog(item) {
  if (item) {
    editedIndex.value = atividades.value.findIndex(a => a.id === item.id)
    const clone = { ...item }
    if (clone.data) clone.data = formatDate(clone.data)
    editedItem.value = clone
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, descricao: '', custo: null, data: '' }
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
      await api.put(`/api/atividade/${payload.id}`, payload)
    } else {
      await api.post('/api/atividade', payload)
    }
    fetchAtividades()
    closeDialog()
    window.dispatchEvent(new CustomEvent('http-success', { detail: 'Atividade salva com sucesso!' }))
  } catch {
    window.dispatchEvent(new CustomEvent('http-error', { detail: 'Erro ao salvar atividade.' }))
  }
}

function confirmDelete(item) {
  if (confirm(`Deseja remover a atividade "${item.descricao}"?`)) {
    api.delete(`/api/atividade/${item.id}`)
      .then(() => {
        fetchAtividades()
        window.dispatchEvent(new CustomEvent('http-success', { detail: 'Atividade removida com sucesso!' }))
      })
      .catch(() => {
        window.dispatchEvent(new CustomEvent('http-error', { detail: 'Erro ao deletar atividade.' }))
      })
  }
}

onMounted(fetchAtividades)
</script>
