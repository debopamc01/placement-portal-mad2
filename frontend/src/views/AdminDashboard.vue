<script setup>
import { onMounted, computed, watch, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import PlacementDriveTable from '@/components/PlacementDriveTable.vue';
import { modifyPlacementDriveStatus } from '@/common/apiFunctions';
import StudentsTable from '@/components/StudentsTable.vue';
import ApplicationsTable from '@/components/ApplicationsTable.vue';
import CompaniesTable from '@/components/CompaniesTable.vue';
import NavBar from '@/components/NavBar.vue';

const router = useRouter();
const authStore = useAuthStore();

const companies = ref([]);
const errorMessage = ref('');
const placementDrives = ref([]);
const students = ref([]);
const applications = ref([]);
const activeTab = ref('companies');
const searchField = ref('');
const searchValue = ref('');

async function loadCompanies() {
  errorMessage.value = '';

  try {
    const response = await fetch('/api/admin/companies', {
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    companies.value = data.data.companies;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to load companies';
  }
}
async function modify_company(companyId, action) {
  const actions = ['approve', 'reject', 'blacklist'];
  if (actions.indexOf(action) === -1) {
    console.error(`Action should be one of ${actions}, but is ${action}`);
    return;
  }
  const url = `/api/admin/company/${companyId}/${action}`;

  try {
    const response = await fetch(url, { method: 'POST', credentials: 'include' });
    const data = await response.json();
    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }
    const company = companies.value.find((company) => company.id === companyId);

    if (company) {
      company.approval_status = data.data.status;
      loadPlacementDrives();
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to ${action} company`;
  }
}
async function loadPlacementDrives() {
  errorMessage.value = '';
  try {
    const response = await fetch('/api/admin/placement-drives', {
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    placementDrives.value = data.data.placement_drives;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to load placement drives';
  }
}

async function modifyPlacementDrive(placementDriveId, action) {
  try {
    const userRole = authStore.user.role.toLowerCase();
    const newPlacementDrive = await modifyPlacementDriveStatus(userRole, placementDriveId, action);
    const existingPlacementDrive = placementDrives.value.find(
      (pd) => pd.id === newPlacementDrive.id,
    );
    if (existingPlacementDrive) Object.assign(existingPlacementDrive, newPlacementDrive);
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to ${action} placement drive`;
  }
}

async function viewPlacementDrive(placementDriveId) {
  router.push(`/placement-drives/${placementDriveId}`);
}

async function viewCompany(companyId) {
  router.push(`/companies/${companyId}`);
}

async function fetchStudents() {
  errorMessage.value = '';

  try {
    const response = await fetch('/api/admin/students', {
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    students.value = data.data.students;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to fetch students';
  }
}

async function viewStudent(studentId) {
  router.push(`/students/${studentId}`);
}

async function downloadResume(studentId) {
  errorMessage.value = '';

  try {
    const url = `/api/admin/students/${studentId}/resume`;

    const response = await fetch(url, {
      credentials: 'include',
    });

    if (!response.ok) {
      errorMessage.value = 'Unable to download resume.';
      return;
    }

    const blob = await response.blob();

    const objectUrl = URL.createObjectURL(blob);

    window.open(objectUrl, '_blank');

    setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to download resume.';
  }
}

async function blacklistStudent(studentId) {
  errorMessage.value = '';

  try {
    const url = `/api/admin/students/${studentId}/blacklist`;
    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      errorMessage.value = 'Unable to blacklist student';
      return;
    }

    const student = students.value.find((student) => student.id === studentId);

    if (student) {
      student.blacklisted = true;
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to blacklist student';
  }
}

async function approveStudent(studentId) {
  errorMessage.value = '';

  try {
    const url = `/api/admin/students/${studentId}/approve`;
    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      errorMessage.value = 'Unable to approve student';
      return;
    }

    const student = students.value.find((student) => student.id === studentId);

    if (student) {
      student.blacklisted = false;
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to approve student';
  }
}

async function fetchApplications() {
  errorMessage.value = '';

  try {
    const response = await fetch('/api/admin/applications', {
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.errors;
      return;
    }

    applications.value = data.data.applications;
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Unable to fetch applications';
  }
}

async function viewApplicationDetails(applicationId) {
  errorMessage.value = '';
  try {
    router.push(`/applications/${applicationId}`);
  } catch (error) {
    console.error(error);
    errorMessage.value = `Unable to view application with id: ${applicationId}`;
  }
}

const searchFields = computed(() => {
  switch (activeTab.value) {
    case 'students':
      return [
        { value: 'name', label: 'Name' },
        { value: 'email', label: 'Email' },
      ];

    case 'companies':
      return [
        { value: 'name', label: 'Name' },
        { value: 'email', label: 'Email' },
        { value: 'approval_status', label: 'Approval Status' },
      ];

    case 'placement-drives':
      return [
        { value: 'job_title', label: 'Job Title' },
        { value: 'status', label: 'Status' },
        { value: 'company_name', label: 'Company Name' },
      ];

    case 'applications':
      return [
        { value: 'student_name', label: 'Student Name' },
        // { value: 'company_name', label: 'Company Name' },
        // TODO: Implement above
        { value: 'status', label: 'Status' },
      ];

    default:
      return [];
  }
});

function clearSearch() {
  searchField.value = '';
  searchValue.value = '';
}

const filteredStudents = computed(() => {
  if (!searchField.value || !searchValue.value) {
    return students.value;
  }

  const searchString = searchValue.value.toLowerCase();

  switch (searchField.value) {
    case 'name':
      return students.value.filter((student) => student.name.toLowerCase().includes(searchString));

    case 'email':
      return students.value.filter((student) => student.email.toLowerCase().includes(searchString));

    default:
      return students.value;
  }
});

const filteredCompanies = computed(() => {
  if (!searchField.value || !searchValue.value) {
    return companies.value;
  }

  const searchString = searchValue.value.toLowerCase();

  switch (searchField.value) {
    case 'name':
      return companies.value.filter((company) => company.name.toLowerCase().includes(searchString));

    case 'email':
      return companies.value.filter((company) =>
        company.email.toLowerCase().includes(searchString),
      );

    case 'approval_status':
      return companies.value.filter((company) =>
        company.approval_status.toLowerCase().includes(searchString),
      );

    default:
      return companies.value;
  }
});

const filteredPlacementDrives = computed(() => {
  if (!searchField.value || !searchValue.value) {
    return placementDrives.value;
  }
  const searchString = searchValue.value.toLowerCase();

  switch (searchField.value) {
    case 'job_title':
      return placementDrives.value.filter((pd) =>
        pd.job_title.toLowerCase().includes(searchString),
      );

    case 'status':
      return placementDrives.value.filter((pd) => pd.status.toLowerCase().includes(searchString));
    case 'company_name':
      return placementDrives.value.filter((pd) =>
        pd.company.name.toLowerCase().includes(searchString),
      );

    default:
      return placementDrives.value;
  }
});

const filteredApplications = computed(() => {
  if (!searchField.value || !searchValue.value) {
    return applications.value;
  }
  const searchString = searchValue.value.toLowerCase();

  switch (searchField.value) {
    case 'student_name':
      return applications.value.filter((app) =>
        app.student.name.toLowerCase().includes(searchString),
      );

    case 'status':
      return applications.value.filter((app) => app.status.toLowerCase().includes(searchString));
    // case 'company_name':
    //   return applications.value.filter((app) =>
    //     app.company.name.toLowerCase().includes(searchString),
    //   );

    default:
      return applications.value;
  }
});

watch(activeTab, () => {
  clearSearch();
});

onMounted(() => {
  authStore.loadUser();
  loadCompanies();
  loadPlacementDrives();
  fetchStudents();
  fetchApplications();
});
</script>

<template>
  <div class="container mt-5">
    <NavBar :title="'Admin Dashboard'" />

    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card shadow-sm text-center">
          <div class="card-body">
            <h6 class="text-muted mb-1">Students</h6>
            <div class="h1">👨‍🎓</div>
            <h2 class="mb-0">{{ students.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm text-center">
          <div class="card-body">
            <h6 class="text-muted mb-1">Companies</h6>
            <div class="h1">🏢</div>
            <h2 class="mb-0">{{ companies.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm text-center">
          <div class="card-body">
            <h6 class="text-muted mb-1">Placement Drives</h6>
            <div class="h1">💼</div>

            <h2 class="mb-0">{{ placementDrives.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm text-center">
          <div class="card-body">
            <h6 class="text-muted mb-1">Applications</h6>
            <div class="h1">📝</div>
            <h2 class="mb-0">{{ applications.length }}</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="container mt-5">
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'companies' }"
            @click="activeTab = 'companies'"
          >
            Companies
          </button>
        </li>

        <li class="nav-item">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'students' }"
            @click="activeTab = 'students'"
          >
            Students
          </button>
        </li>

        <li class="nav-item">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'placement-drives' }"
            @click="activeTab = 'placement-drives'"
          >
            Placement Drives
          </button>
        </li>

        <li class="nav-item">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'applications' }"
            @click="activeTab = 'applications'"
          >
            Applications
          </button>
        </li>
      </ul>
      <div class="mb-4 d-flex justify-content-start gap-2">
        <select v-model="searchField" class="form-select w-auto">
          <option disabled value="">Search By</option>

          <option v-for="field in searchFields" :key="field.value" :value="field.value">
            {{ field.label }}
          </option>
        </select>

        <input v-model="searchValue" class="form-control" placeholder="Search..." />

        <button class="btn btn-primary w-auto">Search</button>

        <button class="btn btn-secondary w-auto" @click="clearSearch">Clear</button>
      </div>
      <CompaniesTable
        v-if="activeTab === 'companies'"
        :companies="filteredCompanies"
        :actions="['view', 'approve', 'reject', 'blacklist']"
        @view="viewCompany"
        @approve="(companyId) => modify_company(companyId, 'approve')"
        @reject="(companyId) => modify_company(companyId, 'reject')"
        @blacklist="(companyId) => modify_company(companyId, 'blacklist')"
      />

      <StudentsTable
        v-if="activeTab === 'students'"
        :students="filteredStudents"
        :actions="['view', 'blacklist', 'approve']"
        @view="viewStudent"
        @blacklist="blacklistStudent"
        @view-resume="downloadResume"
        @approve="approveStudent"
      />

      <div class="mt-4" v-if="activeTab === 'placement-drives'">
        <div class="card shadow-sm">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Placement Drives</h5>
          </div>
          <PlacementDriveTable
            :placement-drives="filteredPlacementDrives"
            :actions="['approve', 'decline', 'reopen', 'close', 'view']"
            :show-company="true"
            @approve="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'approve')"
            @decline="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'decline')"
            @close="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'close')"
            @reopen="(placementDriveId) => modifyPlacementDrive(placementDriveId, 'reopen')"
            @view="viewPlacementDrive"
          />
        </div>
      </div>

      <ApplicationsTable
        v-if="activeTab === 'applications'"
        :applications="filteredApplications"
        :actions="['view']"
        :disable-actions-button="false"
        @view="viewApplicationDetails"
      />
    </div>
  </div>
</template>
