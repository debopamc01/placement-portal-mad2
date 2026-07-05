<script setup>
defineProps({
  status: {
    type: String,
    required: true,
  },
});

function placementDriveStatusBadgeClass(status) {
  switch (status) {
    case 'pending':
      return 'bg-secondary';
    case 'active':
      return 'bg-success';
    case 'declined':
      return 'bg-danger';
    case 'closed':
      return 'bg-dark';
    default:
      return 'bg-light text-dark';
  }
}
</script>

<template>
  <span class="badge fs-6" :class="placementDriveStatusBadgeClass(status)">
    {{ status.toUpperCase() }}
  </span>
</template>
