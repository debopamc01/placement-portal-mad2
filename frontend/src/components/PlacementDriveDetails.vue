<script setup>
import { computed, reactive, watch } from 'vue';
import StatusBadge from '@/components/StatusBadges.vue';

const props = defineProps({
  placementDrive: {
    type: Object,
    default: () => ({
      job_title: '',
      job_description: '',
      eligibility_criteria: '',
      application_deadline: '',
      application_ids: [],
    }),
  },

  mode: {
    type: String,
    default: 'view',
    // supported options: create/edit/view
  },

  loading: {
    type: Boolean,
    default: false,
  },

  showApplicationsCount: {
    type: Boolean,
    default: false,
  },

  allowedActions: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits([
  'create',
  'save',
  'back',
  'approve',
  'decline',
  'close',
  'delete',
  'edit',
  'reopen',
  'apply',
]);

const localPlacementDrive = reactive({
  job_title: '',
  job_description: '',
  eligibility_criteria: '',
  application_deadline: '',
});

watch(
  //source
  () => props.placementDrive,

  //callback
  (drive) => {
    if (!drive) return;

    Object.assign(localPlacementDrive, {
      job_title: drive.job_title ?? '',
      job_description: drive.job_description ?? '',
      eligibility_criteria: drive.eligibility_criteria ?? '',
      application_deadline: to_datetime_local_format(drive.application_deadline) ?? '',
    });
  },

  //options
  { immediate: true },
);

const isReadOnly = computed(() => props.mode === 'view');

const formattedDeadline = computed(() => {
  if (!props.placementDrive?.application_deadline) return '';

  return new Date(props.placementDrive.application_deadline).toLocaleString();
});

function to_datetime_local_format(deadline) {
  if (!deadline) return;
  const date = new Date(deadline);

  const pad = (n) => String(n).padStart(2, '0');

  const formattedDate = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
  return formattedDate;
}

function submit() {
  if (props.mode === 'create') {
    emit('create', { ...localPlacementDrive });
  } else if (props.mode === 'edit') {
    emit('save', { ...localPlacementDrive });
  }
}
</script>

<template>
  <form @submit.prevent="submit">
    <!-- <div class="container py-2"> -->
      <div class="card shadow-sm">
        <!-- Header -->

        <div class="card-header d-flex justify-content-between align-items-center">
          <div>
            <h5 class="mb-1">
              {{
                mode === 'create'
                  ? 'Create Placement Drive'
                  : mode === 'edit'
                    ? 'Edit Placement Drive'
                    : placementDrive.job_title
              }}
            </h5>

            <small v-if="mode !== 'create'" class="text-muted">
              {{ placementDrive.company.name }}
            </small>
          </div>

          <StatusBadge v-if="mode !== 'create'" :status="placementDrive.status" />
        </div>

        <!-- Body -->

        <div class="card-body">
          <div class="mb-4">
            <label class="form-label fw-semibold"> Job Title </label>

            <input
              v-model="localPlacementDrive.job_title"
              :class="isReadOnly ? 'form-control-plaintext' : 'form-control'"
              :readonly="isReadOnly"
              required
            />
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold"> Job Description </label>

            <textarea
              v-model="localPlacementDrive.job_description"
              rows="3"
              class="form-control"
              :readonly="isReadOnly"
              required
            ></textarea>
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold"> Eligibility Criteria </label>

            <textarea
              v-model="localPlacementDrive.eligibility_criteria"
              rows="3"
              class="form-control"
              :readonly="isReadOnly"
              required
            ></textarea>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label fw-semibold"> Application Deadline </label>

              <!--- TODO: Add logic so that deadline cannot be before creation time-->

              <input
                v-if="!isReadOnly"
                type="datetime-local"
                v-model="localPlacementDrive.application_deadline"
                class="form-control"
                required
              />

              <input v-else class="form-control-plaintext" :value="formattedDeadline" readonly />
            </div>

            <div v-if="mode !== 'create' && showApplicationsCount" class="col-md-6 mb-3">
              <label class="form-label fw-semibold"> Applications Received </label>

              <input
                class="form-control-plaintext"
                :value="placementDrive.application_ids.length"
                readonly
              />
            </div>
          </div>
        </div>

        <!-- Footer -->

        <div class="card-footer">
          <div class="d-flex justify-content-end gap-2">
            <!-- Left button -->

            <div class="d-flex gap-2">
              <!-- Create -->

              <button
                v-if="mode === 'create'"
                class="btn btn-primary"
                type="submit"
                :disabled="loading"
              >
                {{ loading ? 'Creating' : 'Create' }}
              </button>

              <!-- Edit -->

              <button
                v-else-if="mode === 'edit'"
                class="btn btn-primary"
                type="submit"
                :disabled="loading"
              >
                {{ loading ? 'Saving' : 'Save Changes' }}
              </button>

              <!-- View -->

              <div
                v-else-if="
                  allowedActions.length > 0 &&
                  !(allowedActions.length === 1 && placementDrive.has_applied)
                "
                class="dropdown"
              >
                <button
                  class="btn btn-outline-primary dropdown-toggle"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Actions
                </button>

                <ul class="dropdown-menu">
                  <li
                    v-if="allowedActions.includes('approve') && placementDrive.status !== 'active'"
                  >
                    <button
                      type="button"
                      class="dropdown-item text-success"
                      @click="$emit('approve')"
                    >
                      Approve
                    </button>
                  </li>

                  <li
                    v-if="
                      allowedActions.includes('decline') && placementDrive.status !== 'declined'
                    "
                  >
                    <button
                      type="button"
                      class="dropdown-item text-danger"
                      @click="$emit('decline')"
                    >
                      Decline
                    </button>
                  </li>

                  <li v-if="allowedActions.includes('edit') && placementDrive.status !== 'closed'">
                    <button type="button" class="dropdown-item text-primary" @click="$emit('edit')">
                      Edit
                    </button>
                  </li>

                  <li v-if="allowedActions.includes('close') && placementDrive.status !== 'closed'">
                    <button
                      type="button"
                      class="dropdown-item text-warning"
                      @click="$emit('close')"
                    >
                      Close
                    </button>
                  </li>

                  <li
                    v-if="allowedActions.includes('reopen') && placementDrive.status === 'closed'"
                  >
                    <button
                      type="button"
                      class="dropdown-item text-success"
                      @click="$emit('reopen')"
                    >
                      Reopen
                    </button>
                  </li>

                  <li v-if="allowedActions.includes('delete')">
                    <hr class="dropdown-divider" />
                  </li>

                  <li v-if="allowedActions.includes('delete')">
                    <button
                      type="button"
                      class="dropdown-item text-danger"
                      @click="$emit('delete')"
                    >
                      Delete
                    </button>
                  </li>

                  <li v-if="allowedActions.includes('apply') && !placementDrive.has_applied">
                    <button
                      type="button"
                      class="dropdown-item text-primary"
                      @click="$emit('apply')"
                    >
                      Apply
                    </button>
                  </li>
                </ul>
              </div>
            </div>
            <!-- Right button -->

            <button
              type="button"
              class="btn btn-secondary"
              :disabled="loading"
              @click="$emit('back')"
            >
              {{ mode === 'view' ? 'Back' : 'Cancel' }}
            </button>
          </div>
        </div>
      </div>
    <!-- </div> -->
  </form>
</template>
