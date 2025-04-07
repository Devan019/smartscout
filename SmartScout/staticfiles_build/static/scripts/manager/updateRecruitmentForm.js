document.addEventListener('DOMContentLoaded', () => {
  const skillInput = document.getElementById('skillInput');
  const skillsContainer = document.getElementById('skillsContainer');
  const skillsField = document.getElementById('skillsField'); // Corrected ID

  let skills = document.getElementById("allskills").innerText;
  let availableSkills = [];
  

  async function datafetch(){
    const response = await fetch('/static/json/skill.json');
    const data = await response.json();
    availableSkills = data.skills;
  }

    async function main(){
      try {
        skills = JSON.parse(skills.replace(/'/g, '"')); 
        // Convert single quotes to double quotes & parse
        
        if (!Array.isArray(skills)) throw new Error();
        
       await datafetch()
      } catch (e) {
      console.log("in catch", e)
        skills = skills.split(',').map(skill => skill.trim().replace(/\[|\]|'/g, '')); 

       }
    
        skills.forEach(skill=>{
          addSkill(skill, true)
          updateHiddenField();
        })
    
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
                      addSkill(skill, true);
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

    

    
  function addSkill(skill, isadd = false) {
    if (isadd) skills = skills.filter(s => s != skill);
      if (skill && availableSkills.includes(skill) && !skills.includes(skill)) {
        console.log("wow")
         if(isadd) skills.push(skill);

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
          
      }
  }


  function updateHiddenField() {
      skillsField.value = JSON.stringify(skills); 
      console.log("wow " , skillsField.value)
      // Store skills as JSON string
  }
    }

    main()
});