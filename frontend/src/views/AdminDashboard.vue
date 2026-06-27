<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const companies = ref([]);
const errorMessage = ref('');

async function logout() {
  await authStore.logout();
  router.push('/login');
}

async function loadCompanies() {
  errorMessage.value = '';

  try {
    const response = await fetch('http://127.0.0.1:5000/api/admin/companies', {
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    companies.value = data.data.companies;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to load companies';
  }
}
async function modify_company(companyId, action) {
  const actions = ['approve', 'reject', 'blacklist'];
  if (actions.indexOf(action) === -1) {
    console.log(`Action should be one of ${actions}, but is ${action}`);
    return;
  }
  const url = `http://127.0.0.1:5000/api/admin/company/${companyId}/${action}`;

  try {
    const response = await fetch(url, { method: 'POST', credentials: 'include' });
    const data = await response.json();
    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    const company = companies.value.find((company) => company.id === companyId);

    if (company) {
      company.approval_status = data.data.status;
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to ${action} company`;
  }
}
onMounted(() => {
  loadCompanies();
});
</script>

<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between">
      <h1>Admin Dashboard</h1>

      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>

    <hr />

    <div v-if="authStore.user">
      <p>
        <strong>Email:</strong>
        {{ authStore.user.email }}
      </p>

      <p>
        <strong>Role:</strong>
        {{ authStore.user.role }}
      </p>
    </div>

    <table v-if="companies.length" class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Website</th>
          <th>Approval Status</th>
          <th>Placement Drives</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="company in companies" :key="company.id">
          <td>{{ company.id }}</td>
          <td>{{ company.name }}</td>
          <td>{{ company.email }}</td>
          <td>
            <a :href="company.website" target="_blank">
              {{ company.website }}
            </a>
          </td>
          <td style="text-transform: uppercase">
            <span
              class="badge"
              :class="{
                'bg-danger': ['rejected', 'blacklisted'].includes(company.approval_status),
                'bg-secondary': company.approval_status === 'pending',
                'bg-success': company.approval_status === 'approved',
              }"
            >
              {{ company.approval_status }}
            </span>
          </td>
          <td>{{ company.placement_drive_ids.length }}</td>
          <td>
            <button
              class="btn btn-sm btn-light dropdown-toggle"
              type="button"
              aria-expanded="false"
              data-bs-toggle="dropdown"
            >
              Actions
            </button>
            <ul class="dropdown-menu">
              <li>
                <button class="dropdown-item">View Details</button>
              </li>
              <li v-if="company.approval_status !== 'approved'">
                <button
                  class="dropdown-item text-success"
                  @click="modify_company(company.id, 'approve')"
                >
                  Approve
                </button>
              </li>
              <li v-if="company.approval_status !== 'rejected'">
                <button
                  class="dropdown-item text-primary"
                  @click="modify_company(company.id, 'reject')"
                >
                  Reject
                </button>
              </li>
              <li v-if="company.approval_status !== 'blacklisted'">
                <button
                  class="dropdown-item text-danger"
                  @click="modify_company(company.id, 'blacklist')"
                >
                  Blacklist
                </button>
              </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="alert alert-info">No companies found.</div>
  </div>
</template>
