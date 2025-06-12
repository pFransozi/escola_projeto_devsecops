<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Notícias</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Nova Notícia</v-btn>
    </v-toolbar>

    <v-data-table
      :columns="headers"
      :items="noticias"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
      loading-text="Carregando notícias..."
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
            {{ editedIndex === -1 ? 'Nova Notícia' : 'Editar Notícia' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedItem.descricao"
              label="Título da Notícia"
              required
            />
            <v-textarea
              v-model="editedItem.conteudo"
              label="Conteúdo"
              rows="5"
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
const noticias = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  descricao: '',
  conteudo: ''
})

// =======================================
// Cabeçalho da tabela
// =======================================
const headers = [
  { text: 'ID',        value: 'id',       align: 'start', width: '80px' },
  { text: 'Título',    value: 'descricao', align: 'start'           },
  { text: 'Ações',     value: 'actions',  sortable: false, align: 'center' }
]

function fetchNoticias() {
  loading.value = true
  api.get('/api/noticia')
    .then(response => {
      noticias.value = response.data.data
    })
    .catch(err => {
      console.error('Erro ao carregar notícias:', err)
    })
    .finally(() => {
      loading.value = false
    })
}

function openDialog(item) {
  if (item) {
    editedIndex.value = noticias.value.findIndex(n => n.id === item.id)
    editedItem.value = { ...item }
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, descricao: '', conteudo: '' }
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
    request = api.put(`/api/noticia/${payload.id}`, payload)
  } else {
    request = api.post('/api/noticia', payload)
  }
  request
    .then(() => {
      fetchNoticias()
      closeDialog()
    })
    .catch(err => {
      alert(err.response?.data?.message || 'Erro ao salvar')
    })
}

function confirmDelete(item) {
  if (confirm(`Deseja remover a notícia "${item.descricao}"?`)) {
    api.delete(`/api/noticia/${item.id}`)
      .then(fetchNoticias)
      .catch(err => alert(err.response?.data?.message || 'Erro ao deletar'))
  }
}

onMounted(fetchNoticias)
</script>
