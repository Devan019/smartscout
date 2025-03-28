document.getElementById('search').addEventListener('input', function () {
  const searchTerm = this.value.toLowerCase()
  const rows = document.querySelectorAll('.profile-row')

  rows.forEach((row) => {
    const name = row.getAttribute('data-name')
    const exp = row.getAttribute('data-exp')
    const skills = row.getAttribute('data-skills')

    if (name.includes(searchTerm) || exp.includes(searchTerm) || skills.includes(searchTerm)) {
      row.classList.remove('hidden')
    } else {
      row.classList.add('hidden')
    }
  })
})

document.getElementById('filter-all').addEventListener('click', function() {
  window.location.href = "?filter=all";
});

document.getElementById('filter-skills').addEventListener('click', function() {
  window.location.href = "?filter=skills";
});

document.getElementById('filter-exp').addEventListener('click', function() {
  window.location.href = "?filter=exp";
});

const urlParams = new URLSearchParams(window.location.search);
const filter = urlParams.get('filter');

if (filter === 'skills') {
  document.getElementById('filter-skills').classList.add('bg-blue-600', 'text-white');
  document.getElementById('filter-skills').classList.remove('bg-gray-700', 'text-gray-300');
} else if (filter === 'exp') {
  document.getElementById('filter-exp').classList.add('bg-blue-600', 'text-white');
  document.getElementById('filter-exp').classList.remove('bg-gray-700', 'text-gray-300');
} else {
  document.getElementById('filter-all').classList.add('bg-blue-600', 'text-white');
}