function showAddManagerForm() {
        
}

function hideAddManagerForm() {
  document.getElementById('manager-form').classList.add('hidden')
}

function editManager(name) {
  console.log()
  
  document.getElementById('manager-form').classList.remove('hidden')
  document.getElementById('form-title').textContent = 'Edit Manager Details ✏️'
  // Prefill fields with manager data (example only)
  document.getElementById('manager-name').value = name
  document.getElementById('manager-email').value = `${name.toLowerCase().replace(/ /g, '.')}@example.com`
  document.getElementById('manager-phone').value = '+1234567890'
}


function deleteManager(name) {
  if (confirm(`Are you sure you want to delete manager: ${name}?`)) {
    // Perform delete action (e.g., send request to server)
    alert(`${name} has been deleted. 🗑️`)
  }
}