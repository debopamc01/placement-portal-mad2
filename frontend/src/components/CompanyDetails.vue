<script setup>
import { computed, reactive, watch } from 'vue';
import StatusBadge from '@/components/StatusBadges.vue';

const props = defineProps({
  company: {
    type: Object,
    default: () => ({
      name: '',
      email: '',
      hr_contact: '',
      website: '',
    }),
  },

  mode: {
    type: String,
    default: 'view',
    // Options: view | edit
  },

  editProfilePermission: {
    type: Boolean,
    default: false,
  },

  allowedActions: {
    type: Array,
    default: () => [],
    // Options: ['approve', 'reject', 'blacklist']
  },
});

const emit = defineEmits(['save', 'back', 'edit', 'approve', 'reject', 'blacklist']);

const localCompany = reactive({
  name: '',
  email: '',
  hr_contact: '',
  website: '',
});

watch(
  () => props.company,
  (company) => {
    if (!company) return;

    Object.assign(localCompany, {
      name: company.name ?? '',
      email: company.email ?? '',
      hr_contact: company.hr_contact ?? '',
      website: company.website ?? '',
    });
  },
  { immediate: true },
);

const isReadOnly = computed(() => props.mode === 'view');

function submit() {
  emit('save', { ...localCompany });
}
</script>

<template>
  <form @submit.prevent="submit">
    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h4 class="mb-0">
          {{ mode === 'edit' ? 'Edit Company Details' : 'Company Details' }}
        </h4>
        <StatusBadge v-if="mode !== 'edit'" :status="company.approval_status" />
      </div>

      <div class="card-body">
        <div class="mb-3">
          <label class="form-label fw-semibold"> Company Name </label>

          <input v-model="localCompany.name" class="form-control" :readonly="isReadOnly" required />
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold"> Email </label>

          <input v-model="localCompany.email" type="email" class="form-control" disabled />
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold"> HR Contact </label>

          <input v-model="localCompany.hr_contact" class="form-control" :readonly="isReadOnly" />
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold"> Website </label>

          <input
            v-model="localCompany.website"
            type="url"
            class="form-control"
            :readonly="isReadOnly"
          />
        </div>
      </div>

      <div class="card-footer d-flex justify-content-end gap-2">
        <button v-if="mode === 'edit'" type="submit" class="btn btn-primary">Save Changes</button>
        <button
          v-if="mode !== 'edit' && editProfilePermission"
          type="button"
          class="btn btn-outline-primary"
          @click="$emit('edit')"
        >
          Edit Profile
        </button>
        <div v-if="allowedActions.length > 0" class="dropdown">
          <button
            class="btn btn-outline-primary dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            Actions
          </button>
          <ul class="dropdown-menu">
            <li v-if="allowedActions.includes('approve') && company.approval_status !== 'approved'">
              <button type="button" class="dropdown-item text-success" @click="$emit('approve')">
                Approve
              </button>
            </li>
            <li v-if="allowedActions.includes('reject') && company.approval_status !== 'rejected'">
              <button type="button" class="dropdown-item text-warning" @click="$emit('reject')">
                Reject
              </button>
            </li>
            <li
              v-if="
                allowedActions.includes('blacklist') && company.approval_status !== 'blacklisted'
              "
            >
              <button type="button" class="dropdown-item text-danger" @click="$emit('blacklist')">
                Blacklist
              </button>
            </li>
          </ul>
        </div>
        <button type="button" class="btn btn-secondary" @click="$emit('back')">
          {{ isReadOnly ? 'Back' : 'Cancel' }}
        </button>
      </div>
    </div>
  </form>
</template>
