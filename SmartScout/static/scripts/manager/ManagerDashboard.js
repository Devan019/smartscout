const employees_data = document.querySelectorAll(".employees-data");
const employees = []
employees_data.forEach((emp,idx) => {
  
  const obj = {
    id : document.querySelectorAll(".id")[idx].value,
    role : document.querySelectorAll(".role")[idx].value,
    exp : document.querySelectorAll(".experience")[idx].value,
    type:document.querySelectorAll(".employee_type")[idx].value,
    salary:document.querySelectorAll(".salary_lpa")[idx].value
  }
  console.log(obj)

  employees.push(obj)
})


let selectedCandidateId = null

function selectCandidate(candidateId) {
  selectedCandidateId = candidateId
  const form = document.getElementById('employeeForm')
  form.action = form.action.split('?')[0] + `?candidate_id=${candidateId}`
}

document.querySelector('.employeeSearch').addEventListener('input', function (e) {
  const searchTerm = e.target.value.toLowerCase()
  const rows = document.querySelectorAll('#employeeTableBody tr.employee-row')

  rows.forEach((row) => {
    const name = row.cells[0].textContent.toLowerCase()
    const email = row.cells[1].textContent.toLowerCase()
    const role = row.cells[2].textContent.toLowerCase()
    const matches = name.includes(searchTerm) || email.includes(searchTerm) || role.includes(searchTerm)
    row.style.display = matches ? '' : 'none'
  })
})

// Candidate search
document.querySelector('.candidateSearch').addEventListener('input', function (e) {
  const searchTerm = e.target.value.toLowerCase()
  const rows = document.querySelectorAll('#profileSelectionModal tbody tr')

  rows.forEach((row) => {
    const name = row.cells[0].textContent.toLowerCase()
    const email = row.cells[1].textContent.toLowerCase()
    const matches = name.includes(searchTerm) || email.includes(searchTerm)
    row.style.display = matches ? '' : 'none'
  })
})
// Toggle modal function
function toggleModal(modalId) {
  const modal = document.getElementById(modalId)
  modal.classList.toggle('hidden')
  document.body.classList.toggle('overflow-hidden', !modal.classList.contains('hidden'))
}

// Close modals when clicking outside
document.querySelectorAll('.modal').forEach((modal) => {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      toggleModal(modal.id)
    }
  })
})

let currentEmployeeId = null

function openEditModal(employeeId) {
  currentEmployeeId = employeeId
  console.log(currentEmployeeId)
  let obj = {}

  for(let emp of employees){
    if(emp.id == currentEmployeeId){
      obj = emp;
      break;
    }
  }
  console.log(obj)

  document.querySelector(".update-role").value = obj.role;
  document.querySelector(".update-exp").value = obj.exp;
  document.querySelector(".update-type").value = obj.type;
  document.querySelector(".update-salary").value = obj.salary;

  const form = document.querySelector("#updateEmployeeForm");
  form.action = form.action.split('?')[0] + `?id=${currentEmployeeId}`
  toggleModal('editEmployeeModal')
}



function confirmDelete(employeeId) {
  currentEmployeeId = employeeId
  const form = document.querySelector("#deleteEmployeeForm");
  form.action = form.action.split('?')[0] + `?id=${currentEmployeeId}`
  toggleModal('deleteConfirmationModal')
}



// Initialize Vanta.js

VANTA.NET({
  el: '.main',
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.0,
  minWidth: 200.0,
  scale: 1.0,
  scaleMobile: 1.0,
  color: 0x3b82f6,
  backgroundColor: 0x0f172a,
  points: 16.0,
  maxDistance: 20.0,
  spacing: 18.0
})