<script setup>
import { ref } from 'vue';

const email = ref('');
const password = ref('');
const errorMessage = ref('');

async function login() {
  errorMessage.value = '';

  try {
    const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    console.log(data);

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    console.log('Login successful');

    const another_response = await fetch('http://127.0.0.1:5000/api/auth/user', {
      credentials: 'include',
    });
    console.log(await another_response.json());
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to contact server';
  }
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <h2 class="mb-4">Login</h2>

        <div class="mb-3">
          <input v-model.lazy="email" class="form-control" placeholder="Email" />
        </div>

        <div class="mb-3">
          <input
            v-model.lazy="password"
            type="password"
            class="form-control"
            placeholder="Password"
          />
        </div>

        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>

        <button class="btn btn-primary" @click="login">Login</button>
      </div>
    </div>
  </div>
</template>
