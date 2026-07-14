<script setup>
import StatusBadge from '@/components/StatusBadges.vue';

defineProps({
  companies: {
    type: Array,
    required: true,
  },

  actions: {
    type: Array,
    default: () => [],
    // Options: ['view', 'approve', 'reject', 'blacklist', 'delete']
  },
});

const emit = defineEmits(['view', 'approve', 'reject', 'blacklist', 'delete']);
</script>

<template>
  <!-- <div class="container py-2"> -->
    <div class="card shadow-sm mt-4">
      <div class="card-header">
        <h5 class="mb-0">Companies</h5>
      </div>

      <div class="card-body p-0">
        <table class="table table-striped table-hover mb-0 align-middle">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Website</th>
              <th>Status</th>
              <th>Placement Drives</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="company in companies" :key="company.id">
              <td>{{ company.id }}</td>

              <td>{{ company.name }}</td>

              <td>{{ company.email }}</td>

              <td>
                <a :href="company.website" target="_blank" rel="noopener noreferrer">
                  {{ company.website }}
                </a>
              </td>

              <td>
                <StatusBadge :status="company.approval_status" :font-size="'fs-7'" />
              </td>

              <td>
                {{ company.placement_drive_ids.length }}
              </td>

              <td class="text-center">
                <div v-if="actions.length > 0" class="dropdown">
                  <button
                    class="btn btn-sm btn-outline-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                  >
                    Actions
                  </button>

                  <ul class="dropdown-menu">
                    <li v-if="actions.includes('view')">
                      <button class="dropdown-item" @click="emit('view', company.id)">
                        View Details
                      </button>
                    </li>

                    <li
                      v-if="actions.includes('approve') && company.approval_status !== 'approved'"
                    >
                      <button
                        class="dropdown-item text-success"
                        @click="emit('approve', company.id)"
                      >
                        Approve
                      </button>
                    </li>

                    <li v-if="actions.includes('reject') && company.approval_status !== 'rejected'">
                      <button
                        class="dropdown-item text-warning"
                        @click="emit('reject', company.id)"
                      >
                        Reject
                      </button>
                    </li>

                    <li
                      v-if="
                        actions.includes('blacklist') && company.approval_status !== 'blacklisted'
                      "
                    >
                      <button
                        class="dropdown-item text-danger"
                        @click="emit('blacklist', company.id)"
                      >
                        Blacklist
                      </button>
                    </li>

                    <template v-if="actions.includes('delete')">
                      <li>
                        <hr class="dropdown-divider" />
                      </li>

                      <li>
                        <button
                          class="dropdown-item text-danger"
                          @click="emit('delete', company.id)"
                        >
                          Delete
                        </button>
                      </li>
                    </template>
                  </ul>
                </div>
              </td>
            </tr>

            <tr v-if="companies.length === 0">
              <td colspan="7" class="text-center text-muted py-4">No companies found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  <!-- </div> -->
</template>
