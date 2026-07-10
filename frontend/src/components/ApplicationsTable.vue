<script setup>
import StatusBadge from '@/components/StatusBadges.vue';

defineProps({
  applications: {
    type: Array,
    required: true,
  },

  actions: {
    type: Array,
    default: () => [],
  },

  disableActionsButton: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(['view', 'shortlist', 'select', 'reject']);
</script>

<template>
  <div class="container py-2">
    <div class="card shadow-sm mt-4">
      <div class="card-header">
        <h4 class="mb-0">Applications</h4>
      </div>

      <div class="card-body p-0">
        <table class="table table-striped table-hover mb-0 align-middle">
          <thead>
            <tr>
              <th>Student</th>
              <th>Email</th>
              <th>Status</th>
              <th>Applied On</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="application in applications" :key="application.id">
              <td>
                {{ application.student.name }}
              </td>

              <td>
                {{ application.student.email }}
              </td>

              <td>
                <StatusBadge :status="application.status" />
              </td>

              <td>
                {{ new Date(application.application_date).toLocaleString() }}
              </td>

              <td class="text-center">
                <div class="dropdown">
                  <button
                    class="btn btn-sm btn-outline-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    :disabled="disableActionsButton"
                  >
                    Actions
                  </button>

                  <ul class="dropdown-menu">
                    <li v-if="actions.includes('view')">
                      <button
                        type="button"
                        class="dropdown-item"
                        @click="emit('view', application.id)"
                      >
                        View Details
                      </button>
                    </li>

                    <li v-if="actions.includes('shortlist') && application.status === 'applied'">
                      <button
                        type="button"
                        class="dropdown-item text-warning"
                        @click="emit('shortlist', application.id)"
                      >
                        Shortlist
                      </button>
                    </li>

                    <li v-if="actions.includes('select') && application.status !== 'selected'">
                      <button
                        type="button"
                        class="dropdown-item text-success"
                        @click="emit('select', application.id)"
                      >
                        Select
                      </button>
                    </li>

                    <li v-if="actions.includes('reject') && application.status !== 'rejected'">
                      <button
                        type="button"
                        class="dropdown-item text-danger"
                        @click="emit('reject', application.id)"
                      >
                        Reject
                      </button>
                    </li>
                  </ul>
                </div>
              </td>
            </tr>

            <tr v-if="applications.length === 0">
              <td colspan="5" class="text-center text-muted py-4">No applications received yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
