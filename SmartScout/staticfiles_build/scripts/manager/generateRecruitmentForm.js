document.addEventListener('DOMContentLoaded', async () => {
  const skillInput = document.getElementById('skillInput');
  const skillsContainer = document.getElementById('skillsContainer');
  const skillsField = document.getElementById('skillsField'); 
  const autoSuggestContainer = document.getElementById('autoSuggestContainer');

  let skills = [];
  let availableSkills = [];

  try {
      const response = await fetch('/static/json/skill.json');
      const data = await response.json();
      availableSkills = data.skills;
  } catch (error) {
      console.error("Error loading skills.json:", error);
  }

  // Show suggestions
  skillInput.addEventListener('input', () => {
      const query = skillInput.value.trim().toLowerCase();
      autoSuggestContainer.innerHTML = '';
      autoSuggestContainer.classList.remove('hidden');

      if (query) {
          const filteredSkills = availableSkills.filter(skill => 
              skill.toLowerCase().includes(query) && !skills.includes(skill)
          );

          filteredSkills.forEach(skill => {
              const suggestion = document.createElement('div');
              suggestion.className = 'px-3 py-2 cursor-pointer hover:bg-gray-700 transition';
              suggestion.textContent = skill;
              suggestion.addEventListener('click', () => {
                  addSkill(skill);
                  skillInput.value = '';
                  autoSuggestContainer.innerHTML = '';
                  autoSuggestContainer.classList.add('hidden');
              });
              autoSuggestContainer.appendChild(suggestion);
          });

          if (filteredSkills.length === 0) {
              autoSuggestContainer.innerHTML = '<div class="px-3 py-2 text-gray-500">No matching skills</div>';
          }
      } else {
          autoSuggestContainer.classList.add('hidden');
      }
  });

  // Hide suggestions when clicking outside
  document.addEventListener('click', (e) => {
      if (!skillInput.contains(e.target) && !autoSuggestContainer.contains(e.target)) {
          autoSuggestContainer.classList.add('hidden');
      }
  });

 
  function addSkill(skill) {
      if (skill && availableSkills.includes(skill) && !skills.includes(skill)) {
          skills.push(skill);

          const skillItem = document.createElement('div');
          skillItem.className = 'flex items-center space-x-2 bg-blue-600 text-white px-3 py-1 rounded-md shadow-md';
          skillItem.innerHTML = `
              <span>${skill}</span>
              <button type="button" class="text-white opacity-70 hover:opacity-100 remove-skill">✖</button>
          `;

          skillItem.querySelector('.remove-skill').addEventListener('click', () => {
              skills = skills.filter(s => s !== skill);
              skillsContainer.removeChild(skillItem);
              updateHiddenField();
          });

          skillsContainer.appendChild(skillItem);
          skillInput.value = '';
          autoSuggestContainer.classList.add('hidden');
          updateHiddenField();
      } else {
          alert(skill ? "Invalid or duplicate skill!" : "Enter a skill.");
      }
  }

  function updateHiddenField() {
      skillsField.value = JSON.stringify(skills);
  }
});