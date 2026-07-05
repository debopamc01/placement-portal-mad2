<script setup>
defineProps({
  status: {
    type: String,
    required: true,
  },
});

const statusClasses = {
  // Placement drives
  pending: 'bg-secondary',
  active: 'bg-success',
  closed: 'bg-dark',
  declined: 'bg-danger',

  // Companies
  approved: 'bg-success',
  blacklisted: 'bg-dark',

  // Applications
  applied: 'bg-primary',
  shortlisted: 'bg-warning text-dark',
  selected: 'bg-success',
  rejected: 'bg-danger',
};

function badgeClass(status) {
  return statusClasses[status] ?? 'bg-light text-dark';
}
</script>

<template>
  <span class="badge fs-6" :class="badgeClass(status)">
    {{ status.toUpperCase() }}
  </span>
</template>
