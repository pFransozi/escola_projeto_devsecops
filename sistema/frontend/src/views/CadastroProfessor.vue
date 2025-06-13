<template>
  <v-container fluid>
    <v-toolbar flat>
      <v-toolbar-title>Cadastro de Professores</v-toolbar-title>
      <v-spacer />
      <v-btn color="primary" @click="openDialog()">Novo Professor</v-btn>
    </v-toolbar>

    <v-data-table
      :headers="headers"
      :items="professores"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
      loading-text="Carregando professores..."
    >
      <!-- Exibe nome do usuário professor -->
      <template #item.nome_usuario="{ item }">
        {{ item.nome_usuario }}
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
            {{ editedIndex === -1 ? 'Novo Professor' : 'Editar Professor' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-row>
              <v-col cols="6">
                <v-select
                  v-model="editedItem.id"
                  :items="usuariosProf"
                  item-title="label"
                  item-value="value"
                  label="Usuário"
                  required
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.salario"
                  label="Salário"
                  type="number"
                  required
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.graduacao"
                  label="Graduação"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.descricao"
                  label="Descrição"
                />
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
const professores = ref([])
const usuariosProf = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  salario: null,
  graduacao: '',
  descricao: ''
})

// Cabeçalhos no padrão Vuetify 3 (Labs)
const headers = [
  { title: 'ID',        key: 'id',           align: 'start', width: '80px' },
  { title: 'Usuário',   key: 'nome_usuario', align: 'start'              },
  { title: 'Salário',   key: 'salario',      align: 'end'                },
  { title: 'Graduação', key: 'graduacao',    align: 'start'              },
  { title: 'Ações',     key: 'actions',      sortable: false, align: 'center' }
]

async function fetchProfessores() {
  loading.value = true
  try {
    const res = await api.get('/api/professor')
    professores.value = res.data.data
  } catch (err) {
    console.error('Erro ao carregar professores:', err)
  } finally {
    loading.value = false
  }
}

async function fetchUsuariosProf() {
  try {
    const res = await api.get('/api/usuario')
    usuariosProf.value = res.data.data
      .filter(u => u.tipo === 'professor')
      .map(u => ({ label: `${u.nome} ${u.ultimo_nome}`, value: u.id }))
  } catch (err) {
    console.error('Erro ao carregar usuários:', err)
  }
}

function openDialog(item) {
  if (item) {
    editedIndex.value = professores.value.findIndex(p => p.id === item.id)
    editedItem.value = { ...item }
  } else {
    editedIndex.value = -1
    editedItem.value = { id: null, salario: null, graduacao: '', descricao: '' }
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
      await api.put(`/api/professor/${payload.id}`, payload)
    } else {
      await api.post('/api/professor', payload)
    }
    await fetchProfessores()
    closeDialog()
  } catch (err) {
    alert(err.response?.data?.message || 'Erro ao salvar')
  }
}

function confirmDelete(item) {
  if (confirm(`Deseja remover o professor ${item.nome_usuario}?`)) {
    api.delete(`/api/professor/${item.id}`)
      .then(fetchProfessores)
      .catch(err => alert(err.response?.data?.message || 'Erro ao deletar'))
  }
}

onMounted(async () => {
  await fetchUsuariosProf()
  await fetchProfessores()
})
</script>
