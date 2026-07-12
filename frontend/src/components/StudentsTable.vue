<script setup>
defineProps({
  students: {
    type: Array,
    required: true,
  },

  actions: {
    type: Array,
    default: () => [],
    // Options: ['view']
  },
});

const emit = defineEmits(['view', 'blacklist', 'delete']);
</script>

<template>
  <div class="container py-2">
    <div class="card shadow-sm mt-5">
      <div class="card-header">
        <h4 class="mb-0">Students</h4>
      </div>

      <div class="card-body p-0">
        <table class="table table-striped table-hover mb-0 align-middle">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Degree</th>
              <th>Department</th>
              <th>CGPA</th>
              <th>Graduation Year</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="student in students" :key="student.id">
              <td>{{ student.name }}</td>

              <td>{{ student.email }}</td>

              <td>{{ student.degree }}</td>

              <td>{{ student.department }}</td>

              <td>{{ student.cgpa }}</td>

              <td>{{ student.graduation_year }}</td>

              <td class="text-center">
                <div v-if="actions.length > 0" class="dropdown">
                  <button
                    class="btn btn-sm btn-outline-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                  >
                    Actions
                  </button>

                  <ul class="dropdown-menu">
                    <li v-if="actions.includes('view')">
                      <button type="button" class="dropdown-item" @click="emit('view', student.id)">
                        View Profile
                      </button>
                    </li>
                    <li v-if="actions.includes('blacklist')">
                      <button
                        type="button"
                        class="dropdown-item text-danger"
                        @click="emit('blacklist', student.id)"
                      >
                        Blacklist
                      </button>
                    </li>
                    <li v-if="actions.includes('delete')">
                      <hr class="dropdown-divider" />
                    </li>
                    <li v-if="actions.includes('delete')">
                      <button
                        class="dropdown-item text-danger"
                        @click="emit('delete', placementDrive.id)"
                      >
                        Delete
                      </button>
                    </li>
                  </ul>
                </div>
              </td>
            </tr>

            <tr v-if="students.length === 0">
              <td colspan="7" class="text-center text-muted py-4">No students found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
