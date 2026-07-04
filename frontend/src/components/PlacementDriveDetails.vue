<script setup>
defineProps({
  placementDrive: {
    type: Object,
    required: true,
  },

  canEdit: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['edit']);
</script>

<template>
  <div class="card shadow-sm border-0">
    <!-- Header -->
    <div class="card-header bg-white py-4">
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <h2 class="mb-1">
            {{ placementDrive.job_title }}
          </h2>

          <div class="text-muted">
            {{ placementDrive.company.name }}
          </div>
        </div>

        <div class="text-end">
          <span
            class="badge fs-6"
            :class="{
              'bg-secondary': placementDrive.status === 'pending',
              'bg-success': placementDrive.status === 'active',
              'bg-danger': placementDrive.status === 'declined',
              'bg-dark': placementDrive.status === 'closed',
            }"
          >
            {{ placementDrive.status }}
          </span>

          <div v-if="canEdit" class="mt-3">
            <button class="btn btn-outline-primary" @click="emit('edit', placementDrive.id)">
              Edit Placement Drive
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Body -->
    <div class="card-body">
      <div class="row g-4">
        <div class="col-lg-8">
          <h5>Job Description</h5>

          <p class="text-muted">
            {{ placementDrive.job_description }}
          </p>

          <hr />

          <h5>Eligibility Criteria</h5>

          <p class="text-muted">
            {{ placementDrive.eligibility_criteria }}
          </p>
        </div>

        <div class="col-lg-4">
          <div class="card bg-light border-0">
            <div class="card-body">
              <h5 class="card-title mb-4">Summary</h5>

              <div class="mb-3">
                <small class="text-muted d-block"> Application Deadline </small>

                <strong>
                  {{ placementDrive.application_deadline }}
                </strong>
              </div>

              <div class="mb-3">
                <small class="text-muted d-block"> Applications Received </small>

                <strong>
                  {{ placementDrive.application_ids.length }}
                </strong>
              </div>

              <div>
                <small class="text-muted d-block"> Company </small>

                <strong>
                  {{ placementDrive.company.name }}
                </strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
