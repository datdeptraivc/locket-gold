const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

// date of birth
document.addEventListener('DOMContentLoaded', function() {
	var dobInput = document.getElementById('register-dob');
	dobInput.addEventListener('focus', function() {
		this.type = 'date'; // Khi trường nhập được tập trung vào, chuyển kiểu dữ liệu sang 'date'
		this.classList.remove('placeholder'); // Xóa lớp CSS mô phỏng placeholder
	});

	dobInput.addEventListener('blur', function() {
		if (this.value === '') {
			this.type = 'text'; // Nếu không có giá trị, chuyển kiểu dữ liệu về lại 'text'
			this.classList.add('placeholder'); // Thêm lớp CSS mô phỏng placeholder
		}
	});
});