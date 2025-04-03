async function main() {

  let availableSkills = [];

  try {
    const response = await fetch('/static/json/skill.json');
    const data = await response.json();
    availableSkills = data.skills;
  } catch (error) {
    console.error("Error loading skills.json:", error);
  }

  return availableSkills;
}
const createTeamBtn = document.getElementById('createTeamBtn')
const createTeamModal = document.getElementById('createTeamModal')
const closeModal = document.getElementById('closeModal')
const cancelCreate = document.getElementById('cancelCreate')

const editTeamModal = document.getElementById('editTeamModal')
const closeEditModal = document.getElementById('closeEditModal')
const cancelEdit = document.getElementById('cancelEdit')

const team_names = document.querySelectorAll(".team_name")
const project_names = document.querySelectorAll(".project_name")
const project_descriptions = document.querySelectorAll(".project_description")
const all_skills = document.querySelectorAll(".skills")
const ids = document.querySelectorAll(".team_id")

//all teams
// Build teams array with member emails
let teams = [];

team_names.forEach((ele, idx) => {
  // Get all member elements for this team
  const memberElements = document.querySelectorAll(`.team_id[value="${ids[idx].value}"] ~ .members`);
  
  // Extract just the email part (after team ID)
  const members = Array.from(memberElements).map(el => {
    const fullText = el.innerText;
    return fullText.replace(/^\d+/, ''); // Remove team ID prefix
  });

  let obj = {
    id: ids[idx].value,
    team_name: team_names[idx].value,
    project_name: project_names[idx].value,
    skills: all_skills[idx].innerText,
    members: members, // Array of member emails
    desc: project_descriptions[idx].value
  };
  teams.push(obj);
});

console.log("Teams data:", teams); // Verify member emails are captured
// Then in openEditModal
function openEditModal(teamId) {
  const team = teams.find(t => t.id == teamId);
  if (team) {
    document.querySelectorAll('#editEmployeeList input[type="checkbox"]').forEach(checkbox => {
      checkbox.checked = team.members.includes(checkbox.value);
    });
  }
}

console.log(teams)
// Update the edit form submission
document.getElementById('editTeamForm').addEventListener('submit', function(e) {
  // Collect all selected skills from the edit modal
  const skillElements = document.querySelectorAll('#editSkillsContainer span');
  const skills = Array.from(skillElements).map(el => 
    el.textContent.trim().replace(/\s+/g, ' ')
  );
  
  // Create a hidden input if it doesn't exist
  let skillsInput = document.querySelector('#editTeamForm input[name="skills"]');
  if (!skillsInput) {
    skillsInput = document.createElement('input');
    skillsInput.type = 'hidden';
    skillsInput.name = 'skills';
    this.appendChild(skillsInput);
  }
  skillsInput.value = skills.join(',');
});
// Create modal handlers
createTeamBtn.addEventListener('click', () => {
  createTeamModal.classList.remove('hidden')
})

closeModal.addEventListener('click', () => {
  createTeamModal.classList.add('hidden')
})

cancelCreate.addEventListener('click', () => {
  createTeamModal.classList.add('hidden')
})

// Edit modal handlers
function openEditModal(teamId) {
  // Reset modal
  document.querySelector("#editSkillsContainer").innerHTML = '';
  document.getElementById('editTeamId').value = teamId;
  
  // Find the team
  const team = teams.find(t => t.id == teamId);
  if (!team) {
    console.error("Team not found:", teamId);
    return;
  }

  // Populate basic info
  document.querySelector("#editProjectName").value = team.project_name;
  document.querySelector("#editTeamName").value = team.team_name;
  document.querySelector("#editTeamDesc").value = team.desc;

  // Populate skills
  try {
    const skills = JSON.parse(team.skills.replace(/'/g, '"'));
    const editModalIndex = 1; // Assuming index 1 is for edit modal
    skills.forEach(skill => addSkill(skill, editModalIndex, true));
  } catch (e) {
    console.error("Error parsing skills:", e);
  }

  // Check checkboxes for team members
  const checkboxes = document.querySelectorAll('#editEmployeeList input[type="checkbox"]');
  console.log(`Found ${checkboxes.length} checkboxes for team ${teamId}`);
  
  checkboxes.forEach(checkbox => {
    const email = checkbox.value.trim();
    const isMember = team.members.some(memberEmail => 
      memberEmail.trim() === email
    );
    checkbox.checked = isMember;
    console.log(`Checkbox ${email} checked: ${isMember}`);
  });

  // Show modal

  const form = document.querySelector("#editTeamForm");
  form.action = form.action.split('?')[0] + `?id=${teamId}`

  editTeamModal.classList.remove('hidden');
}
closeEditModal.addEventListener('click', () => {
  editTeamModal.classList.add('hidden')
})

cancelEdit.addEventListener('click', () => {
  editTeamModal.classList.add('hidden')
})



document.getElementById('teamForm').addEventListener('submit', function (e) {
  // Collect all selected skills
  const skillElements = document.querySelectorAll('#skillsContainer span');
  const skills = Array.from(skillElements).map(el =>
    el.textContent.trim().replace(/\s+/g, ' ')
  );
  document.getElementById('skillsHiddenInput').value = skills.join(',');

  // The members will be automatically included via the checkboxes
});
// Employee search functionality (for both modals)
function setupEmployeeSearch(searchId, listId) {
  const searchInput = document.getElementById(searchId)
  const employeeList = document.getElementById(listId)
  const employeeItems = employeeList.querySelectorAll('.employee-item')

  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase()

    employeeItems.forEach((item) => {
      const name = item.querySelector('label span:first-child').textContent.toLowerCase()
      const details = item.querySelector('label span:last-child').textContent.toLowerCase()

      if (name.includes(searchTerm) || details.includes(searchTerm)) {
        item.style.display = 'flex'
      } else {
        item.style.display = 'none'
      }
    })
  })
}

// Initialize search for both modals
setupEmployeeSearch('memberSearch', 'employeeList')
setupEmployeeSearch('editMemberSearch', 'editEmployeeList')


const skillInputs = document.querySelectorAll('.skillInputs');
const skillsContainers = document.querySelectorAll('.skillsContainers');
const skillsFields = document.querySelectorAll('.skillsFields');
const autoSuggestContainers = document.querySelectorAll('.autoSuggestContainers');

let skills = [];
let availableSkills = []
main()
  .then((data) => {
    // skills = data
    availableSkills = data;
  })
// Show suggestions
skillInputs.forEach((ele, idx) => ele.addEventListener('input', () => {
  const query = ele.value.trim().toLowerCase();
  autoSuggestContainers[idx].innerHTML = '';
  autoSuggestContainers[idx].classList.remove('hidden');

  if (query) {
    const filteredSkills = availableSkills.filter(skill =>
      skill.toLowerCase().includes(query) && !skills.includes(skill)
    );

    filteredSkills.forEach(skill => {
      const suggestion = document.createElement('div');
      suggestion.className = 'px-3 py-2 cursor-pointer hover:bg-gray-700 transition';
      suggestion.textContent = skill;
      suggestion.addEventListener('click', () => {
        addSkill(skill, idx);
        skillInputs[idx].value = '';
        autoSuggestContainers[idx].innerHTML = '';
        autoSuggestContainers[idx].classList.add('hidden');
      });
      autoSuggestContainers[idx].appendChild(suggestion);
    });

    if (filteredSkills.length === 0) {
      autoSuggestContainers[idx].innerHTML = '<div class="px-3 py-2 text-gray-500">No matching skills</div>';
    }
  } else {
    autoSuggestContainers[idx].classList.add('hidden');
  }
}));

// Hide suggestions when clicking outside
document.addEventListener('click', (e) => {


  autoSuggestContainers.forEach((ele, idx) => {
    if (skillInputs[idx].contains(e.target) && ele.contains(e.target)) {
      ele.classList.add('hidden')
    }
  })

});


function addSkill(skill, idx, isadd) {
  if (isadd) skills = skills.filter(s => s != skill);
  if (skill && availableSkills.includes(skill) && !skills.includes(skill)) {
    console.log("wow")
    if (isadd) skills.push(skill);

    const skillItem = document.createElement('div');
    skillItem.className = 'flex items-center space-x-2 bg-blue-600 text-white px-3 py-1 rounded-md shadow-md';
    skillItem.innerHTML = `
              <span>${skill}</span>
              <button type="button" class="text-white opacity-70 hover:opacity-100 remove-skill">✖</button>
          `;

    skillItem.querySelector('.remove-skill').addEventListener('click', () => {
      skills = skills.filter(s => s !== skill);
      skillsContainers[idx].removeChild(skillItem);
    });

    skillsContainers[idx].appendChild(skillItem);
    skillInputs[idx].value = '';
    autoSuggestContainers[idx].classList.add('hidden');
  }
}

function confirmDelete(id, deleteUrl) {
  if(confirm("Confirm to delete.")) {
      window.location.href = deleteUrl.replace('0', id);
  }
}


function toggleTeamStatus(id, toggleUrl) {
  window.location.href = toggleUrl.replace('0', id);
}