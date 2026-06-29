<script setup>
defineProps({
  placementDrives: {
    type: Array,
    required: true,
  },

  actions: {
    type: Array,
    required: true,
  },

  showCompany: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits([
  'approve',
  'decline',
  'close',
  'reopen',
  'edit',
  'delete',
  'view',
  'apply',
]);

function statusClass(status) {
  switch (status) {
    case 'pending':
      return 'bg-secondary';

    case 'active':
      return 'bg-success';

    case 'closed':
      return 'bg-dark';

    case 'declined':
      return 'bg-danger';

    default:
      return 'bg-light text-dark';
  }
}
</script>

<template>
  <table class="table table-striped table-hover align-middle">
    <thead>
      <tr>
        <th v-if="showCompany">Company</th>
        <th>Job Title</th>
        <th>Application Deadline</th>
        <th>Status</th>
        <th>Applications</th>
        <th>Actions</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="placementDrive in placementDrives" :key="placementDrive.id">
        <td v-if="showCompany">
          {{ placementDrive.company.name }}
        </td>

        <td>{{ placementDrive.job_title }}</td>

        <td>{{ placementDrive.application_deadline }}</td>

        <td style="text-transform: uppercase">
          <span class="badge" :class="statusClass(placementDrive.status)">
            {{ placementDrive.status }}
          </span>
        </td>
        <!--- TODO: Make the above and the below fields dynamic-->

        <td>{{ placementDrive.application_ids.length }}</td>

        <td>
          <button
            class="btn btn-sm btn-light dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            Actions
          </button>

          <ul class="dropdown-menu">
            <li>
              <button class="dropdown-item" @click="emit('view', placementDrive.id)">
                View Details
              </button>
            </li>
            <li v-if="placementDrive.status !== 'active' && actions.indexOf('approve') != -1">
              <button
                class="dropdown-item text-success"
                @click="emit('approve', placementDrive.id)"
              >
                Approve
              </button>
            </li>

            <li v-if="placementDrive.status !== 'declined' && actions.indexOf('decline') != -1">
              <button class="dropdown-item text-danger" @click="emit('decline', placementDrive.id)">
                Decline
              </button>
            </li>

            <li v-if="placementDrive.status !== 'closed' && actions.indexOf('close') != -1">
              <button class="dropdown-item text-warning" @click="emit('close', placementDrive.id)">
                Close
              </button>
            </li>

            <li v-if="placementDrive.status === 'closed' && actions.indexOf('reopen') != -1">
              <button class="dropdown-item text-success" @click="emit('reopen', placementDrive.id)">
                Reopen
              </button>
            </li>

            <li v-if="placementDrive.status !== 'closed' && actions.indexOf('edit') != -1">
              <button class="dropdown-item text-primary" @click="emit('edit', placementDrive.id)">
                Edit
              </button>
            </li>

            <li v-if="actions.indexOf('delete') != -1">
              <button class="dropdown-item text-danger" @click="emit('delete', placementDrive.id)">
                Delete
              </button>
            </li>
            <li v-if="actions.indexOf('apply') != -1">
              <button class="dropdown-item btn-primary" @click="emit('apply', placementDrive.id)">
                Apply
              </button>
            </li>
          </ul>
        </td>
      </tr>

      <tr v-if="placementDrives.length === 0">
        <td :colspan="showCompany ? 6 : 5" class="text-center text-muted">
          No placement drives found.
        </td>
      </tr>
    </tbody>
  </table>
</template>
