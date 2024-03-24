document.addEventListener("DOMContentLoaded", function() {
    var dropdownToggle = document.getElementById("dropdown-toggle");
    var dropdownMenu = document.getElementById("dropdown-menu");
  
    dropdownToggle.addEventListener("click", function(event) {
      dropdownToggle.classList.toggle('open'); // Thêm hoặc xóa class 'open'
      if (dropdownToggle.classList.contains('open')) {
        dropdownMenu.style.visibility = "visible";
        dropdownMenu.style.opacity = "1";
      } else {
        dropdownMenu.style.visibility = "hidden";
        dropdownMenu.style.opacity = "0";
      }
    });
  
    // Hide dropdown menu when clicking outside of it
    document.addEventListener("click", function(event) {
      if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.style.visibility = "hidden";
        dropdownMenu.style.opacity = "0";
        dropdownToggle.classList.remove('open');
      }
    });
  });