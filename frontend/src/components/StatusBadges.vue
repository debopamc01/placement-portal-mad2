<script setup>
defineProps({
  status: {
    type: String,
    required: true,
  },
  fontSize: {
    type: String,
    default: 'fs-6',
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
  <span class="badge" :class="[badgeClass(status), fontSize]">
    {{ status.toUpperCase() }}
  </span>
</template>
