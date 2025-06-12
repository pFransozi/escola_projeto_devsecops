<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Atividades Escolares</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Nova Atividade Escolar</v-btn>
    </v-toolbar>

    <v-data-table :columns="headers" :items="atividadesEscolares" :items-per-page="10" class="elevation-1"
      :loading="loading" loading-text="Carregando atividades...">
      <!-- Exibe descrição da turma vinculada -->
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
            {{ editedIndex === -1 ? 'Nova Atividade Escolar' : 'Editar Atividade Escolar' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field v-model="editedItem.descricao" label="Descrição da Atividade" required />
            <v-select v-model="editedItem.turma_id" :items="turmasOptions" item-title="label" item-value="value"
              label="Turma" required />
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
const atividadesEscolares = ref([])
const turmasOptions = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  descricao: '',
  turma_id: null
})

const headers = [
  { text: 'ID', value: 'id', align: 'start', width: '80px' },
  { text: 'Descrição', value: 'descricao', align: 'start' },
  { text: 'Turma', value: 'turma_descricao', align: 'start' },
  { text: 'Ações', value: 'actions', sortable: false, align: 'center' }
]

async function fetchTurmas() {
  try {
    const res = await api.get('/api/turma')
    turmasOptions.value = res.data.data.map(t => ({
      label: `${t.descricao} (${t.sala})`,
      value: t.id
    }))
  } catch (err) {
    console.error('Erro ao carregar turmas:', err)
  }
}

async function fetchAtividadesEscolares() {
  loading.value = true
  try {
    const res = await api.get('/api/atividade_escolar')
    atividadesEscolares.value = res.data.data
  } catch (err) {
    console.error('Erro ao carregar atividades escolares:', err)
  } finally {
    loading.value = false
  }
}

function openDialog(item) {
  if (item) {
    editedIndex.value = atividadesEscolares.value.findIndex(a => a.id === item.id)
    editedItem.value = { ...item }
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, descricao: '', turma_id: null }
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
      await api.put(`/api/atividade_escolar/${payload.id}`, payload)
    } else {
      await api.post('/api/atividade_escolar', payload)
    }
    await fetchAtividadesEscolares()
    closeDialog()
  } catch (err) {
    alert(err.response?.data?.message || 'Erro ao salvar')
  }
}

function confirmDelete(item) {
  if (confirm(`Deseja remover a atividade "${item.descricao}"?`)) {
    api.delete(`/api/atividade_escolar/${item.id}`)
      .then(fetchAtividadesEscolares)
      .catch(err => alert(err.response?.data?.message || 'Erro ao deletar'))
  }
}

onMounted(async () => {
  await fetchTurmas()
  await fetchAtividadesEscolares()
})
</script>
