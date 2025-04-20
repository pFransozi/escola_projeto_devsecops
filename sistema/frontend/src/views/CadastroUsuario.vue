<template>
    <v-container class="mt-8" max-width="600px">
        <v-card>
            <v-card-title class="text-h5">Cadastro de Usuário</v-card-title>
            <v-card-text>
                <v-form @submit.prevent="cadastrarUsuario" ref="formRef">
                    <v-row dense>
                        <v-col cols="6">
                            <v-text-field v-model="form.nome" label="Nome" required />
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="form.ultimo_nome" label="Último Nome" required />
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="form.usuario" label="Usuário" required />
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="form.senha" label="Senha" type="password" required />
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="form.email" label="Email" />
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="form.data_nascimento" label="Data de Nascimento" type="date"
                                required />
                        </v-col>
                        <v-col cols="6">
                            <v-select v-model="form.sexo" label="Sexo" :items="['M', 'F']" required />
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="form.cpf" label="CPF" required />
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="form.endereco" label="Endereço" required />
                        </v-col>
                        <v-col cols="12">
                            <v-select v-model="form.tipo" label="Tipo de Usuário" :items="tipos" required />
                        </v-col>
                    </v-row>

                    <v-btn color="primary" type="submit" class="mt-4" :loading="loading" block>
                        Cadastrar
                    </v-btn>

                    <v-alert v-if="erro" type="error" class="mt-4">{{ erro }}</v-alert>
                    <v-alert v-if="sucesso" type="success" class="mt-4">Usuário cadastrado com sucesso!</v-alert>
                </v-form>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>

import {ref} from 'vue'
import axios from 'axios'

const form = ref({
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

const tipos = ['admin', 'secretario', 'professor']

const loading = ref(false)
const sucesso = ref(false)
const erro = ref(null)

async function cadastrarUsuario() {
  erro.value = null
  sucesso.value = false
  loading.value = true

  try {
    const res = await axios.post(import.meta.env.VITE_API_URL + '/usuario', form.value)

    if (res.data.success) {
      sucesso.value = true
      erro.value = null
      form.value = {
        nome: '', ultimo_nome: '', usuario: '', senha: '', email: '',
        data_nascimento: '', sexo: '', cpf: '', endereco: '', tipo: ''
      }
    } else {
      erro.value = res.data.message || 'Erro ao cadastrar usuário.'
    }

  } catch (err) {
    erro.value = err.response?.data?.message || 'Erro ao cadastrar usuário.'
  } finally {
    loading.value = false
  }
}

</script>