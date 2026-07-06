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

  showApplicationStatus: {
    type: Boolean,
    default: false,
  },

  showPlacementDriveStatus: {
    type: Boolean,
    default: true,
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

function placementDriveStatusClass(status) {
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

function jobApplicationStatusClass(status) {
  switch (status) {
    case 'applied':
      return 'bg-primary';

    case 'shortlisted':
      return 'bg-warning text-dark';

    case 'selected':
      return 'bg-success';

    case 'rejected':
      return 'bg-danger';

    default:
      return 'bg-secondary';
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
        <th v-if="showPlacementDriveStatus">Status</th>
        <th v-if="!showApplicationStatus">Applications</th>
        <th v-if="showApplicationStatus">Application Status</th>
        <th>Actions</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="placementDrive in placementDrives" :key="placementDrive.id">
        <td v-if="showCompany">
          {{ placementDrive.company.name }}
        </td>

        <td>{{ placementDrive.job_title }}</td>

        <td>{{ new Date(placementDrive.application_deadline).toLocaleString() }}</td>

        <td v-if="showPlacementDriveStatus" style="text-transform: uppercase">
          <span class="badge" :class="placementDriveStatusClass(placementDrive.status)">
            {{ placementDrive.status }}
          </span>
        </td>
        <!--- TODO: Make the above and the below fields dynamic-->

        <td v-if="!showApplicationStatus">{{ placementDrive.application_ids.length }}</td>

        <td v-if="showApplicationStatus" style="text-transform: uppercase">
          <span
            v-if="placementDrive.has_applied"
            class="badge"
            :class="jobApplicationStatusClass(placementDrive.application_status)"
          >
            {{ placementDrive.application_status }}
          </span>
          <span v-else class="badge bg-secondary">Not Applied</span>
        </td>

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
            <li v-if="actions.indexOf('apply') != -1 && !placementDrive.has_applied">
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
