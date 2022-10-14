function logout() {
	fetch("http://localhost:8000/logout/", {
		method: "post",
		body: "",
	}).then((response) => {
		window.location.href = '/login/';
	});
}