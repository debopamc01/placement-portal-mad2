import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);

  const isAuthenticated = computed(() => user.value !== null);

  async function loadUser() {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/auth/user', {
        credentials: 'include',
      });

      const data = await response.json();

      if (response.ok) {
        user.value = data.data.user;
      } else {
        user.value = null;
      }
    } catch {
      user.value = null;
    }
  }

  async function login(email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.errors);
    }

    await loadUser();
  }

  async function logout() {
    await fetch('http://127.0.0.1:5000/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    });

    user.value = null;
  }

  return {
    user,
    isAuthenticated,
    login,
    logout,
    loadUser,
  };
});
