<script setup>
import { computed, reactive, watch } from 'vue';

const props = defineProps({
  student: {
    type: Object,
    default: () => ({
      name: '',
      email: '',
      description: '',
      cgpa: '',
      degree: '',
      department: '',
      graduation_year: '',
    }),
  },

  mode: {
    type: String,
    default: 'view', // view | edit
  },
});

const emit = defineEmits(['save', 'back']);

const localStudent = reactive({
  name: '',
  email: '',
  description: '',
  cgpa: '',
  degree: '',
  department: '',
  graduation_year: '',
});

watch(
  () => props.student,
  (student) => {
    if (!student) return;

    Object.assign(localStudent, {
      name: student.name ?? '',
      email: student.email ?? '',
      description: student.description ?? '',
      cgpa: student.cgpa ?? '',
      degree: student.degree ?? '',
      department: student.department ?? '',
      graduation_year: student.graduation_year ?? '',
    });
  },
  { immediate: true },
);

const isReadOnly = computed(() => props.mode === 'view');

function submit() {
  emit('save', { ...localStudent });
}
</script>

<template>
  <form @submit.prevent="submit">
    <div class="card shadow-sm">
      <div class="card-header">
        <h4 class="mb-0">
          {{ mode === 'edit' ? 'Edit Student Details' : 'Student Details' }}
        </h4>
      </div>

      <!---TODO: Update with actual fields-->

      <div class="card-body">
        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold"> Name </label>

            <input
              v-model="localStudent.name"
              class="form-control"
              :readonly="isReadOnly"
              required
            />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold"> Email </label>

            <input
              v-model="localStudent.email"
              type="email"
              class="form-control"
              :readonly="isReadOnly"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold"> Description </label>

          <textarea
            v-model="localStudent.description"
            rows="4"
            class="form-control"
            :readonly="isReadOnly"
          ></textarea>
        </div>

        <div class="row">
          <div class="col-md-4 mb-3">
            <label class="form-label fw-semibold"> CGPA </label>

            <input
              v-model="localStudent.cgpa"
              type="number"
              step="0.01"
              min="0"
              max="10"
              class="form-control"
              :readonly="isReadOnly"
            />
          </div>

          <div class="col-md-4 mb-3">
            <label class="form-label fw-semibold"> Degree </label>

            <input v-model="localStudent.degree" class="form-control" :readonly="isReadOnly" />
          </div>

          <div class="col-md-4 mb-3">
            <label class="form-label fw-semibold"> Department </label>

            <input v-model="localStudent.department" class="form-control" :readonly="isReadOnly" />
          </div>
        </div>

        <div class="row">
          <div class="col-md-4 mb-3">
            <label class="form-label fw-semibold"> Graduation Year </label>

            <input
              v-model="localStudent.graduation_year"
              type="number"
              class="form-control"
              :readonly="isReadOnly"
            />
          </div>

          <!-- Placeholder for future resume upload -->
          <div class="col-md-8 mb-3">
            <label class="form-label fw-semibold"> Resume </label>

            <div class="form-control-plaintext text-muted">Resume upload coming soon.</div>
          </div>
        </div>
      </div>

      <div class="card-footer d-flex justify-content-between">
        <button type="button" class="btn btn-secondary" @click="$emit('back')">
          {{ isReadOnly ? 'Back' : 'Cancel' }}
        </button>

        <button v-if="mode === 'edit'" type="submit" class="btn btn-primary">Save Changes</button>
      </div>
    </div>
  </form>
</template>
