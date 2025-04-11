function previewImage(event) {
  const reader = new FileReader()
  reader.onload = function () {
    document.getElementById('profile-preview').src = reader.result
  }
  reader.readAsDataURL(event.target.files[0])
}